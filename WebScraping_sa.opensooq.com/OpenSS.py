import requests #استخراج معلومات صفحة الويب
from bs4 import BeautifulSoup as BS #استخراج معلومات صفحة الويب
import pandas as pd #csv تحويل جوسون الى اكسل و
from googletrans import Translator #ترجمت اسم الشركة وعدد الكيلو مترات من عربي الى انقليزي
import json #للتعامل مع ملفات جوسون

print('''
Version: 20.8.21

    Developed by: Awiteb
    GitHub: Awiteb
    Email: Awiteb@hotmail.com
''')
"اخذ اسامي الملفات المراد حفظها"
csvFileName = input(" Enter name of csv file: ").replace(".csv" , '')
jsonFileName = input("\n Enter name of json file: ").replace(".json" , '')
excelFileName = input("\n Enter name of excel file: ").replace(".xls" , '')

pageNumber = int(input("\n Enter number of pages: "))#اخذ رقم الصفحة المراد ايقاف جمع البيانات عندها

fileJson = open(jsonFileName+'.json', 'w', encoding='utf8')#انشاء ملف جوسون للكتابة عليه
fileJson.write('[\n')#كتابة بداية المصفوفة
data = {}#انشاء دكشنري لحفظ البيانات

totalCar = 0#انشاء متغير لجمع عدد السيارات
url = 'https://sa.opensooq.com/ar/%D8%AD%D8%B1%D8%A7%D8%AC-%D8%A7%D9%84%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA/%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D9%84%D9%84%D8%A8%D9%8A%D8%B9?page='

for page in range(pageNumber):
    page += 1#للبداية من صفحة رقم واحد وليس صفر والانتها عند الصفحة التي ادخلت رقمها
    print(f" Total cars: {totalCar}")#طباعة مجموع السيارات التي تم جمعها
    urlAndPage = url + str(page)#اضافة رقم الصفحة الى الرابط
    print("---" , page , "---")#طباعة رقم الصفحة
    print(urlAndPage)#طباعة الرابط الذي سوف يتم استخراج البيانات منه
    r = requests.get(urlAndPage)
    soup = BS(r.content , 'html.parser') #اخذ الكود المصدري للصفحة لاستخراج البيانات منه
    cars = soup.findAll('li' , {'class' : "rectLi ie relative mb15"})#اخذ مجموعة من الكلاسات بنفس الاسم لاحتوائها على معلومات السيارات التي بالصفحة

    for pC in cars:#بعد اخذ مجموعة الكلاسات يتم تفريدها هنا بمتغير (بي سي) وهو اختصار ل خصائص السيارة
        if pC.find('span', {'class': 'inline vMiddle postSpanTitle'}) and pC.find('span', {'class': 'inline ltr'}) and pC.findAll('li' , {'class' : "ml8"}) and pC.find('span' , {'class' : "inline vMiddle"}):#هاذا الشرط بمعنى اذا تواجدة هاذي الخصائص نفذ الأتي
            name = pC.find('span' , {'class': "inline vMiddle postSpanTitle"})#اسم السيارة يتواجد في هاذا الكلاس
            if len(name.text) > 37:#اذا كان اسم السيارة اكثر من 37 حرف يتم استبعادها لفلترة مجموع السيارات
                pass#عدم فعل شي = استبعادها
            else:
                city = pC.find('span' , {'class' : "inline vMiddle"})#اخذ اسم المدينة من كلاس معين
                carProperties = pC.findAll('li' , {'class' : "ml8"})#جمع جميع خصاص السيارة
                carPrise = pC.find('span', {'class': 'inline ltr'})#اخذ سعر السيارة من كلاس معين وتتم فلترته
                carPrise = carPrise.text.replace(',' , '')#ازالة الفاصلة لتحويل السعر من نص الى رقم
                carPrise = float(carPrise)#تحويل الرقم الى فلوت لازالة الاعداد العشرية وتحويله الى رقم صحيح
                carPrise = '{:.0f}'.format(carPrise)#ازالة الاعداد العشرية ان وجدت
                carPrise = int(carPrise)#ثم تحويله لى عدد صحيح
                """هناك بعض المستخدمين يضعون سعر السيارة مثلأ 16 وهو يقصد 16000 فتتم معالجة هاذا الخلل عبر الكود الاتي"""

                if carPrise < 1000:#اذا كان سعر السيارة اقل من الف افعل الأتي
                    carPrise = str(carPrise) + '000' #تحويل السعر الى نص وزيادة عليه ثلاث اصفار
                    carPrise = int(carPrise)#تحويله الى عدد صحيح من جديد
                else:
                    if len(carProperties) == 4:#اذا السيارة لديها 4 خصائص افعل لأتي لان بعض الناس مايضيفو السعر او الممشى
                        carBrandAr = carProperties[1].text#اخذ شركة السيارة بالعربي
                        if carBrandAr == 'نيسان':#في ترجمة اسم الشركة تتم ترجمة نيسان الى ابريل لتفادي المشكلة يتم تعين الاسم من هنا
                            carBrandEn = 'Nissan'#تعين الاسم بالانقليزي
                        elif carBrandAr == 'لكزس':# لكزس تتم ترجمته الى لكزس لتفادي المشكلة يتم تعينه هنا
                            carBrandEn = 'Lexus'
                        elif carBrandAr == "بورجوارد":#نفس مشكلة اللكزس
                            carBrandEn = "Borgward"
                        else:#اذا كانت الشركة ليست نيسان او لكزس او بورجوارد ترجمه
                            carBrandEn = Translator().translate(carBrandAr)#ترجمه الشركة
                            carBrandEn = carBrandEn.text#اخذ اسم الشركة الانقليزي من الترجمة عشان الترجم تعطيك اللغة المترجم اليها وحنا نحتاج بس النص
                        carModel = carProperties[2].text.replace('أقدم من ' , '')#بعض السيارات يكون قبل الموديل اقدم من (لتفادي المشكة ان وجدت)ء
                        carModel = int(carModel)#تحويل الموديل الا رقم صحيح بعد ازالة اقدم من ان وجدت
                        carKm = carProperties[3].text#اخذ عدد الكيلو مترات للسيارة
                        carKm = str(carKm+' م')#هناك مشكلة في تحويل عدد الكيلو مترات ويجيب اضافة حرف عربي ومسافة
                        carKm = Translator().translate(carKm)#ترجمة عدد كيلو المترات مع حرف الميم والمسافة
                        carKm = carKm.text[ : -2]#ازالة حرف الميم والمسافة بعد الترجمة
                        '''بعد جمع بينات السيارة يجب تخزينها'''
                        data['Name'] = name.text#تخزين اسم السيارة
                        data['Brand'] = carBrandEn#تخزين اسم الشركة بعد ترجمته
                        data['Model'] = carModel#تخزين الموديل بعد فلترته
                        data['Km'] = carKm#تخزين عدد كيلو مترات بعد ترجمته
                        data['Prise'] = carPrise#تخزين السعر بعد فلترته
                        data['City'] = city.text#تخزين اسم المدينة

                        dataJson = json.dumps(data , ensure_ascii=False)#تعريف بينات السيارة ك جيسون
                        fileJson.write(dataJson + ',\n')#حفظ البينات بعد تخزينها

                        totalCar += 1  #اضف واحد الى مجموع السيارات الذي تم تعريفه في الاعلى
                    else:#لاتفعل شي اذا كان عدد خصائص السيارة اقل من 4
                        pass
fileJson.close()#اغلق ملف الجوسون

readJson = open(jsonFileName+'.json' , 'r', encoding='utf8')#فتح ملف الجوسون من جديد للقرائة
stringJson = readJson.read()#اخذ البينات وتخزينها في متغير
readJson.close()#اغلاق الجوسون بعد اخذ البينات
editJson = stringJson.strip(',\n')#التعديل على البينات وازالة اخر فاصلة
fileJson = open(jsonFileName+'.json', 'w', encoding='utf8')#فتح ملف الجوسون من جديد للكتابة
fileJson.write(editJson + '\n]')#اضافة البيانات بعد تعديلها
fileJson.close#اغلاق الملف
print(f"\n\n Done save all data on {jsonFileName}.json")
readJson = pd.read_json(f"{jsonFileName}.json")#قرأت ملف الجوسون بعد اغلاقه لتفادي المشاكل
readJson.to_csv(f"{csvFileName}.csv")#(csv)تحويل ملف الجوسون الى
print(f"\n\n Done save all data on {csvFileName}.csv")
readJson.to_excel(f"{excelFileName}.xls")#(excel)تحويل ملف الجوسون الى
print(f"\n\n Done save all data on {excelFileName}.xls")
