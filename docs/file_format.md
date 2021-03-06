## Формат файлов данных и конфгураций

### Конфигурационный файл config.ini

Конфигурация хранится в ini файле, формат представлен ниже:

[vars]

site_description =  - описание объекта, значение должно быть написано латиницей, значение согласуется с коллегами, которые настраивают CUCM

output_filename_prefix =  - префикс имен исходящих файлов

default_site_operator =  - Оператор по умолчанию для ДАННОГО объекта - используется когда не получается определить имя опрератора по номеру

rdp_css =  - css используемы для создания RDP - будет отличаться от объекта к объекту

forward_all_destination_prefix = ### - css используемы для создания RDP - будет отличаться от объекта к объекту

pickup_group_start_number = 400 -  номер с которого будут начинаться номера pickup групп - надо проверить какой СЕЙЧАС последний в CUCM и поставить на 1 больше

analog_line_access_pt = Pt_SYS_RF_Pref_CUBE_AON -  название партиции, которое используется при создании трансофрмаций, если абонент выходит в город через аналоговые линии (для него указан analog_access_code в файле input_data) С большой долей вероятности не поменяется.

check_inbound_group_number = y -  флаг, указывает проверять ли вхоядщие и исходящие номера на наличие в группе "общих" номеров. прямой не прямой номер. По умолчанию стоит y - проверять. Значения y\n

check_outbound_group_number = y -  флаг, указывает проверять ли вхоядщие и исходящие номера на наличие в группе "общих" номеров. прямой не прямой номер. По умолчанию стоит y - проверять. Значения y\n



[oper_partition_name] - список партиций для опретаоров - Будет отличаться от объекта к объекту, значение согласуется с коллегами, которые настраивают CUCM

[oper_device_pool_name] - список девайс пулов для операторов - Будет отличаться от объекта к объекту, значение согласуется с коллегами, которые настраивают CUCM

[oper_name] - Что получаем из справочника операторов и как его потом используем. Важно чтобы имена справа совпадали с именами в других секциях данного файла.

[oper_transformation_mask] - Для каждого из известных операторов связи указывается количество цифр справа, коорые будут применяться как маска в callingpartytransparent. Или значение Full - весь номер без изменений. На момент создания такой функционал нужен только для номеров ГазСвязи - нужны последние 5 цифр. 4957190102 -> 90102


### Файл данных input_data.csv

Файл содержит инфорацию об абонентах, номерах, моделях телефонов:

name,internal_number,dect_number,ftmn_number,phone_model,inbound_number,outbound_number,old_site_prefix,new_site_prefix

 - name - ФИО абонента - Иванов Иван Иванович, если телефон "общественный" формат записи - Москва Охрана 1 - **обязательное поле**
 - internal_number - короткий номер абонента - **обязательное поле**
 - dect_number - номер дект телефона. если есть - **необязательное поле**
 - ftmn_number - мобильный номер телеофна, если есть - **необязательное поле**
 - phone_model - планируемая модель телефона для абонента - **обязательное поле**
 - inbound_number - прямой городской номер, если есть - **необязательное поле** - формат записи любой (с пробелами, скобками, дефисом)
 - outbound_number - АОН которым закрывается пользователь при выходе в город - **необязательное поле** - формат записи любой (с пробелами, скобками, дефисом)
 - old_site_prefix - префикс объекта (филиала/ДО) до смены - **необязательное поле**
 - new_site_prefix - целевой префикс объекта (филиала/ДО) - **обязательное поле**
 - analog_access_code - код доступа к аналоговой линии/группе линий - выдается нам телефонистами авайя - описывается в листе "Исходящие линии префиксы" опросного листа - **необязательное поле**
 
 
 ### Файл данных input_pickup.csv
 
 Файл содержит инфорацию о группах подхвата и абонентах в них входящих:
 Формат файла соответсвует листу в опросном листе, который заполняется филиалом.
 
 HuntGroup_number,HuntGroup_Name,Ab1,Ab2,Ab3,Ab4,Ab5,Ab6,Ab7,Ab8,Ab9,Ab10
 
 - HuntGroup_number - номер хант группы на станции филиала - **необязательное поле**, при подготовке данных  не используется
 - HuntGroup_Name - имя хант группы на станции филиала - **необязательное поле**, при подготовке данных  не используется
 - Ab1-Ab10 - перечень коротких номеров абонентов, входящих в группу - **обязательное поле**, хотя бы один абонент должен быть указан.
 