# cucm_bulk
Генератор csv файлов для групповой загрузки данных в БД АТС CUCM.
(Данная конфигурация входных\выходных файлов подготовлена под задачи определнного проекта, но может быть расширена для задач других проектов)

## Общее описание

Для генерации выходных файлов необходимо наличие файла конфигураций *config.ini* и 
файла входных данных *input_data.csv* в директории *data*.

Всего ходе работы ПО понадобятся файлы:

 - *input_data.csv* в директории *data*  - файл создается руками из опросного листа филиала. 
 - *config.ini* - значения переменных в файле меняются руками от объекта к объекту.
 - **Export_phones_* в директории *data* - файл выгружается с CUCM поле загрузки файла телефонов.
 - *input_pickup.csv* в директории *data* - файл создается руками из опросного листа филиала.
 - *ad_users.txt* в директории *directory* - справочник пользователей AD и их телефонов.
 - *Kod4.csv* и *Kod8.csv* в директории *directory* - справочники операторов связи, взятые с сайта минкомсвязи. 
 - **_phones_model.csv* в директории *output* - файлы телефонов для загрузки в CUCM,
 генрируются на первом этапе работы ПО и используются позднее.
 
 На основании входных файлов данных и справочников, ПО генерирует выходные файлы в формате, 
 готовом к загрузке в CUCM.
 
 На каждом шаге работы ПО, пользвателю выводится инфораци об используемых файлах и конфигурационных опциях для 
 ознакомления и корректировки. По заврешении операции на экран выводится статистика по данной опреации, 
 и создаются выходные файлы, а также файлы содержащие необработанные (по каким-либо причинам) записи.
 
## Какие данные для загрузки готовит ПО
 
 В ходе работы создаются файлы для загрузки:
 
  - Телефоны  - **_phones_model.csv* 
  - Обновление пользователей - **_Update_Users.csv*
  - Представлене линий - **_Line_apearance.csv*
  - Remote Destiation Profiles - **_RDP.csv*
  - Remote destinations - **_RD.csv*
  - Трансляции - *translationpattern.csv*
  - Трансформации - *callingpartytransparent.csv*
  - Группы подхвата - **_pickup_groups.csv*
  - Членство в группах подхвата - **_pickups.csv*
  
## Какие дополнительные данные готовятся в процессе работы
 
 В ходе работы готовятся:
 
  - Список операторов представленных на данном объекте, опертаоры определяются по входящим и исходящим номерам телеофнов.
  - На каждой операции подготовки выходного csv, гоовится файл содержащий необработанные по какой-либо причине данные с указанием причины (по возможности)
  
## Алгоритм работы с инструментом
 
 (Инструкция с примерами описана ниже)
 1. На основании опросного листа необходимо приготовить файл входных данных *input_data.csv*
 1. На основании опросного листа и натсроек CUCM заполнить конфигурационный файл *config.ini*
 1. Опционально - запустить ПО, в меню выбрать пункт 8 - Show list of operators on the site, дождаться отображения на экране списка операторов связи и настроек CUCM
 1. Подготовить **файлы телефонов** к загрузке в CUCM 
    1. Запустить ПО (если еще не запущено), в меню выбрать пункт 1 - **Construct phones files**
    1. На эеране отобразится подменю с указанием используемх файлов и натсроек. Если все корректно, нажать y.  Если нет, ввести любой другой символ и скорректировать данные в файлах.
    1. На экране отобразится набор строк записанных в выходной файл, а также статистика по данной операции.
    1. В директории output будут созадны файлы для моделей телефонов (по представленным во входном файле моделям) и файл **_unassoiciated_dn.csv*
    1. Проверить файл **_unassoiciated_dn.csv* на наличие записей. Если там есть записи скорее всего что-то не так с входными данными.
    1. Если проблем не обнаружено - файлы **_phones_model.csv* готовы к загрузке в CUCM
    
    
 1. Подготовить **файлы пользователей и представления линий** к загрузке в CUCM
    1. Скопировать файл, выгруженный из CUCM, в директорию *data* - **Важно** имя файла должно содержать *Export_phones*
    1. Убедиться что файлы моделей телефонов, созданные на шаге 4, остались в директории *output*
    1. Запустить ПО (если еще не запущено), в меню выбрать пункт 2 - **Construct user_update and line_appearance files**
    1. На эеране отобразится подменю с указанием используемх файлов и натсроек. Если все корректно, нажать y.  Если нет, ввести любой другой символ и скорректировать данные в файлах.
    1. На экране отобразится набор строк записанных в выходной файл, а также статистика по данной операции.
    1. В директории output будут созадны файлы *_Update_Users.csv*, **_line_apearance.csv* и файл **_unassoiciated_users.csv*
    1. Проверить файл **_unassoiciated_dn.csv* на наличие записей. Если там есть записи, то либо что-то не так с входными данными, либо в справочнике не найден пользователь AD для данного номера. (тонкий момент - некоторые филиалы присылают нам имена пользователей ad, но их может не быть в CUCM, поэтому в ходе работы мы опираемся на справочник который есть в CUCM)
    1. Если проблем не обнаружено - файлы *_Update_Users.csv* и **_line_apearance.csv* готовы к загрузке в CUCM
 
 1. Подготовить **RDP и RD** файлы к загрузке в CUCM
    1. Убедиться что файлы моделей телефонов, созданные на шаге 4, остались в директории *output*
    1. Запустить ПО (если еще не запущено), в меню выбрать пункт 3 - **Construct RD and RDP files**
    1. На эеране отобразится подменю с указанием используемх файлов и натсроек. Если все корректно, нажать y.  Если нет, ввести любой другой символ и скорректировать данные в файлах.
    1. На экране отобразится набор строк записанных в выходной файл, а также статистика по данной операции.
    1. В директории output будут созадны файлы **_RDP.csv*, **_RD.csv* и **_RDP_Unresolved.csv*
    1. Проверить файл **_RDP_Unresolved.csv* на наличие записей. Если там есть записи, то что-то не так с входными данными.
    1. Если проблем не обнаружено - файлы *_RDP.csv* и **_RD.csv* готовы к загрузке в CUCM
 
 1. Подготовить файлы **трансляций и трансформаций** к загрузке в CUCM
    1. Запустить ПО (если еще не запущено), в меню выбрать пункт 4 - **Construct translation and transformation files.**
    1. На эеране отобразится подменю с указанием используемх файлов и натсроек. Если все корректно, нажать y.  Если нет, ввести любой другой символ и скорректировать данные в файлах.
    1. На экране отобразится набор строк записанных в выходной файл, а также статистика по данной операции.
    1. В директории output будут созадны файлы **callingpartytransparent.csv* и **translationpattern.csv* 
    1. Файлы *callingpartytransparent.csv* и *translationpattern.csv*  готовы к загрузке в CUCM
 
 1. Подготовить **файлы пикап групп** к загрузке в CUCM
    1. На основании опросного листа необходимо приготовить файл входных данных *input_pickups.csv*
    1. Запустить ПО (если еще не запущено), в меню выбрать пункт 5 - **Construct pickup group files**
    1. На эеране отобразится подменю с указанием используемх файлов и натсроек. Если все корректно, нажать y.  Если нет, ввести любой другой символ и скорректировать данные в файлах.
    1. На экране отобразится набор строк записанных в выходной файл, а также статистика по данной операции.
    1. В директории output будут созадны файлы **_pickup_groups.csv*, **_pickups.csv* и **_unassociated_pickups.csv*
    1. Проверить файл **_unassociated_pickups.csv* на наличие записей. Если там есть записи, то что-то не так с входными данными.
    1. Если проблем не обнаружено - файлы *_pickup_groups.csv* и **_pickups.csv* готовы к загрузке в CUCM. Загрузка этих данных производится через AXL
 
 1. #######TODO Дописать Backup
 
 
 [Формат файлов](.\docs\file_format.md)
 
 [Установка\запуск](.\docs\install.md)
 
 [Пример работы](.\example.md)
 