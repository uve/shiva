var CoreModule;
(function (CoreModule) {
    var Error = (function () {
        function Error(message, id, callback) {
            this.message = message;

            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Ошибка",
                text: this.message,
                className: "error",
                buttons: {
                    "OK": function () {
                        form.close();
                        if (form.parent_id && !callback && (form.id != form.parent_id)) {
                            form.open(form.parent_id);
                        }
                        if (callback) {
                            callback();
                        }
                    }
                }
            });

            if (id) {
                document.getElementById(id).innerText = this.message;
            }
        }
        return Error;
    })();
    CoreModule.Error = Error;

    var Info = (function () {
        function Info(message, id, callback) {
            this.message = message;

            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Сообщение",
                text: this.message,
                className: "info",
                buttons: {
                    "OK": function () {
                        form.close();
                        if (form.parent_id && !callback && (form.id != form.parent_id)) {
                            form.open(form.parent_id);
                        }
                        if (callback) {
                            callback();
                        }
                    }
                }
            });

            if (id) {
                document.getElementById(id).innerText = this.message;
            }
        }
        return Info;
    })();
    CoreModule.Info = Info;

    var Scanner = (function () {
        function Scanner(callback) {
            var _this = this;
            this.callback = callback;

            DatalogicScanner1.style.visibility = "hidden";
            DatalogicScanner1.style.width = 1;
            DatalogicScanner1.style.height = 1;

            this.DefaultBarcodeType = "EAN 13";

            this.scanhandler_object = function () {
                return (_this.ScanHandler());
            };

            this.init();
        }
        Scanner.prototype.init = function () {
            try  {
                DatalogicScanner1.bScanEnabled = true;
                DatalogicScanner1.attachEvent("LabelScanned", this.scanhandler_object);
            } catch (e) {
                //new Error("DatalogicScanner1 not found 1");
            }
        };

        Scanner.prototype.detach = function () {
            try  {
                DatalogicScanner1.bScanEnabled = false;
                DatalogicScanner1.detachEvent("LabelScanned", this.scanhandler_object);
            } catch (e) {
                //new Error("DatalogicScanner1 not found 2");
            }
        };

        Scanner.prototype.ScanHandler = function () {
            var input = document.getElementById("InputBarcode");

            //alert(input.toString());
            input.value = DatalogicScanner1.sLabelText;

            this.detach();

            this.callback.call(this);
        };
        return Scanner;
    })();
    CoreModule.Scanner = Scanner;

    var Barcode = (function () {
        function Barcode() {
            this.BCTUSER = 1;
            this.BCTPALLET = 2;
            this.BCTCELL = 3;
            this.BCTDELIVERY = 5;
            this.BCTPARTY = 7;
        }
        Barcode.prototype.set = function (value) {
            try  {
                this.isValidBarcodeType(value, this.type);
                this.isEqualExpected(value, this.type, this.expected);

                this.value = this.BarcodeToID(value); //Если нужно вырезать ID
                return true;
            } catch (err) {
                var error = new Error(err, "EnterBarcodeErrText");
                return false;
            }
        };

        Barcode.prototype.BarcodeToID = function (barcode) {
            if (!barcode)
                return "";

            /* Для этих типов не извлекать id-шник */
            if ((this.type == this.BCTUSER) || (this.type == this.BCTCELL) || (!this.type)) {
                return barcode;
            }

            var n = barcode.length;
            var ID = (n >= 11) ? Number(barcode.substring(1, 12)) : barcode;
            return ID.toString();
        };

        // проверка ШК на внутренний тип
        Barcode.prototype.isValidBarcodeType = function (barcode, expectedType) {
            if (barcode.length < 4) {
                throw "неправильная длина штрихкода (минимум 4)";
            }

            if (!expectedType) {
                //new Error("No expected Type");
                return true;
            }
            var n = Number(barcode.toString().substring(0, 1));

            if (n != expectedType) {
                switch (expectedType) {
                    case this.BCTUSER:
                        throw "ожидается ШК пользователя";
                        break;
                    case this.BCTPALLET:
                        throw "ожидается ШК паллеты";
                        break;
                    case this.BCTCELL:
                        throw "ожидается ШК ячейки";
                        break;
                    case this.BCTDELIVERY:
                        throw "ожидается ШК сборочного";
                        break;
                    case this.BCTPARTY:
                        throw "ожидается ШК партии";
                        break;
                    default:
                        throw "Неизвестная ошибка ШК";
                }
                //NewInnerText("EnterBarcodeErrText", errtext);
                //return false;
            } else {
                return true;
            }
        };

        // проверка ШК на ожинаемое значение
        Barcode.prototype.isEqualExpected = function (barcode, expectedType, expected) {
            if (!expectedType) {
                //new Error("No expected Type");
                return true;
            }

            if (!expected) {
                return true;
            }

            if (barcode.toString().substring(0, 10) != expected.toString().substring(0, 10)) {
                switch (expectedType) {
                    case this.BCTUSER:
                        throw "Введён неправильный штрих-код пользователя";
                        break;
                    case this.BCTPALLET:
                        throw "Введён неправильный штрих-код паллеты";
                        break;
                    case this.BCTCELL:
                        throw "Введён неправильный штрих-код ячейки";
                        break;
                    case this.BCTDELIVERY:
                        throw "Введён неправильный штрих-код сборочного";
                        break;
                    case this.BCTPARTY:
                        throw "Введён неправильный штрих-код партии";
                        break;
                    default:
                        throw "Неизвестная ошибка ШК";
                }
                //NewInnerText("EnterBarcodeErrText", errtext);
                //return false;
            } else {
                return true;
            }
        };
        return Barcode;
    })();
    CoreModule.Barcode = Barcode;

    var Core = (function () {
        function Core() {
            this.barcode = new Barcode();

            this.SERVER_TIMEOUT = 1000;

            this.timeout_callback = null;
        }
        Core.prototype.write = function (message) {
            try  {
                console.log(message);
            } catch (e) {
                //alert(message);
            }
        };

        Core.prototype.info = function (message) {
            try  {
                console.log(message, this);
            } catch (e) {
                //alert(message);
            }
        };

        /*
        * Кодирование данных (простого ассоциативного массива вида
        * { name : value, ...} в  URL-escaped строку (кодировка UTF-8)
        */
        Core.prototype.urlEncodeData = function (data) {
            var query = [];
            if (data instanceof Object) {
                for (var k in data) {
                    query.push(encodeURIComponent(k) + "=" + encodeURIComponent(data[k]));
                }
                return query.join('&');
            } else {
                return encodeURIComponent(data);
            }
        };

        Core.prototype.createRequestObject = function () {
            if (typeof XMLHttpRequest != 'undefined') {
                return new XMLHttpRequest();
            }

            var progIDs = [
                'Msxml2.XMLHTTP.6.0',
                'Msxml2.XMLHTTP.5.0',
                'Msxml2.XMLHTTP.4.0',
                'Msxml2.XMLHTTP.3.0',
                'Msxml2.XMLHTTP',
                'Microsoft.XMLHTTP'];

            for (var i = 0; i < progIDs.length; i++) {
                try  {
                    var xmlhttp = new ActiveXObject(progIDs[i]);

                    return xmlhttp;
                } catch (e) {
                }
            }
        };

        Core.prototype.start_loading = function () {
            var form = new FormModule.Form();
            form.open("loading");

            window.scrollTo(0, 0);
        };

        Core.prototype.stop_loading = function () {
            var preloader_id = "loading";
            document.getElementById(preloader_id).style.display = 'none';
        };

        Core.prototype.new_event = function () {
            try  {
                Device.BlinkGreenLed(50, 20, true, true);
            } catch (e) {
            }

            // отобразим текст задания и проиграем звук
            document.getElementById("sound_element").innerHTML = "<embed src='/static/beam.wav' hidden=true autostart=true loop=false>";
        };

        /**
        * Аналог асинхронного вызова из jQuery.ajax
        */
        Core.prototype.ajax = function (settings) {
            var _this = this;
            if (!settings.hidden) {
                this.start_loading();
            }

            var xmlhttp = this.createRequestObject();

            xmlhttp.onreadystatechange = function () {
                var readyState = 9;
                var status = 9;

                try  {
                    readyState = xmlhttp.readyState;
                    status = xmlhttp.status;
                } catch (e) {
                }

                /*
                var point = document.getElementById("point-status");
                point.innerHTML =  point.innerHTML + readyState + '.' + status + '</br>';
                */
                if (readyState != 4)
                    return;

                clearTimeout(_this.timeout_callback);

                if (TORNADO_HASH != xmlhttp.getResponseHeader("tornado_hash")) {
                    IS_RELOAD = true;
                }

                if (!settings.hidden) {
                    _this.stop_loading();
                }

                if (xmlhttp.status == 200) {
                    // Все ок
                    if (xmlhttp.responseText) {
                        var result = eval('(' + xmlhttp.responseText + ')');

                        if (result.error) {
                            if (!settings.hidden) {
                                var error = new Error(result.error, "", function () {
                                    settings.error();
                                });
                            }
                            return;
                        }

                        if (result.info) {
                            if (!settings.hidden) {
                                var info = new Info(result.info, "", function () {
                                    settings.success(result);
                                });
                            }
                            return;
                        }
                    }

                    settings.success(result);
                } else {
                    if (settings.hidden) {
                        return false;
                    }

                    var msg = (xmlhttp.statusText != 'Unknown') ? xmlhttp.statusText : "Нет связи с сервером, проверьте интернет-соединение";

                    var error = new Error(msg, "", function () {
                        settings.error();
                    });
                }
            };

            xmlhttp.open(settings.type, settings.url, true);

            xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            for (var item in settings.data) {
                if (typeof settings.data[item] === "undefined") {
                    delete settings.data[item];
                }
            }

            xmlhttp.send(this.urlEncodeData(settings.data));
            /*
            this.timeout_callback = setTimeout( () => {
            
            xmlhttp.abort();
            xmlhttp.abort();
            
            }, this.SERVER_TIMEOUT);
            
            */
        };

        Core.prototype.application_reload = function () {
            if (IS_RELOAD == "true" || IS_RELOAD == true) {
                location.reload(true);
            }
        };

        Core.prototype.extend = function (destination, source) {
            for (var property in source) {
                if (source.hasOwnProperty(property)) {
                    destination[property] = source[property];
                }
            }
            return destination;
        };
        return Core;
    })();
    CoreModule.Core = Core;
})(CoreModule || (CoreModule = {}));
var FormModule;
(function (FormModule) {
    var Form = (function () {
        function Form() {
            this.DATE_FORMAT = "dd.mm.yyyy";
            this.CURRENT_YEAR = 2013;
        }
        Form.prototype.getElementsByClassName = function (className) {
            var found = [];
            var elements = document.getElementsByTagName("*");
            for (var i = 0; i < elements.length; i++) {
                var names = elements[i].className.split(' ');
                for (var j = 0; j < names.length; j++) {
                    if (names[j] == className)
                        found.push(elements[i]);
                }
            }
            return found;
        };

        Form.prototype.open = function (item) {
            var elements = this.getElementsByClassName('win');
            for (var i = 0; i < elements.length; i++) {
                if (elements[i].style.display == 'block') {
                    elements[i].style.display = 'none';
                    this.parent_id = elements[i].getAttribute("id");
                    /*
                    console.log("this.parent_id");
                    console.log(this.parent_id);
                    */
                }
            }
            document.getElementById(item).style.display = 'block';
            //console.log('open: ' + this.id);
        };

        Form.prototype.close = function () {
            document.getElementById(this.id).style.display = 'none';
            //this.open("FrontWindow2");
            //console.log('close: ' + this.id);
        };

        /*
        * Вызов формы ошибки
        *
        */
        Form.prototype.FormError = function (settings) {
            var _this = this;
            // MsgText - текст сообщения, содержащий HTML-разметку
            // btnText - текст на кнопке
            // func - JS-код, навешиваемый на событие onclick этой кнопки
            this.id = "ErrorMessage1";

            this.open(this.id);

            document.getElementById("ErrorMessageText1").innerHTML = settings.text;

            document.getElementById("form-1").className = "win error";

            var buttonOK = document.getElementById("btnErrorMessage1OK");

            buttonOK.onclick = function () {
                _this.close();
                _this.open(_this.parent_id);
                settings.apply();
            };

            buttonOK.setAttribute("value", "OK");

            buttonOK.focus();
        };

        // вызов универсальной формы ввода штрихкода
        Form.prototype.FormBarcode = function (settings) {
            var _this = this;
            this.id = settings.id;

            if (!settings.id) {
                this.id = "FormBarcode";
            }

            // alert(form.id);
            // settings - объект, имеющий свойства:
            //     text - текст сообщения, содержащий HTML-разметку
            //     expectedType - ожидаемый тип ШК, определяемый самым 1-м символом.
            //         1 - пользователь системы
            //         2 - паллета
            //         3 - ячейка
            //         7 - партия
            //     ApplyOnScan - Флаг: вызов обработчика apply сразу после сканирования
            //     minlength - минимальная длина строки, содержащей ШК (по умолчанию = 1)
            //     maxlength - максимальная длина строки, содержащей ШК (по умолчанию = 13)
            //     apply - JS-код обработчика, навешиваемый на событие onclick кнопки #1
            //     cancel - JS-код обработчика, навешиваемый на событие onclick кнопки #2
            document.getElementById("EnterBarcode").style.backgroundColor = "";

            if (settings.backgroundColor) {
                document.getElementById("EnterBarcode").style.backgroundColor = settings.backgroundColor;
            }

            document.getElementById("caption-2").innerHTML = "";
            document.getElementById("caption-2").style.display = "none";
            document.getElementById("text-2").innerHTML = "";
            document.getElementById("text-2").style.display = "none";

            if (settings.caption) {
                document.getElementById("caption-2").innerHTML = settings.caption;
                document.getElementById("caption-2").style.display = "block";
            }

            if (settings.text) {
                document.getElementById("text-2").innerHTML = settings.text;
                document.getElementById("text-2").style.display = "block";
            }

            //(<HTMLElement>document.getElementById("EnterBarcodeFormText")).innerHTML = settings.text;
            document.getElementById("EnterBarcodeErrText").innerHTML = "";

            // откроем форму и отобразим поясняющий текст
            this.open("EnterBarcode");

            var input = document.getElementById("InputBarcode");
            input.value = "";

            //input.focus();
            var buttonOK = document.getElementById("btnEnterBarcodeOK");
            var buttonCancel = document.getElementById("btnEnterBarcodeCancel");

            buttonOK.removeAttribute("disabled");
            buttonCancel.removeAttribute("disabled");

            buttonOK.onclick = function () {
                //buttonOK.focus();
                _this.scanner.detach();

                //buttonOK.setAttribute("disabled", "disabled");
                //buttonCancel.setAttribute("disabled", "disabled");
                // разрешён переход на функцию apply сразу по вводу ШК
                if (settings.ApplyOnScan) {
                    settings.apply(input.value);
                }
            };

            buttonCancel.onclick = function () {
                //buttonOK.setAttribute("disabled", "disabled");
                //buttonCancel.setAttribute("disabled", "disabled");
                _this.scanner.detach();
                settings.cancel();
            };

            this.scanner = new CoreModule.Scanner(buttonOK.onclick);
        };

        Form.prototype.get_timestamp = function () {
            return (this.get_date().getTime() / 1e3).toString();
        };

        Form.prototype.get_date = function () {
            var new_date = new Date();

            var year = this.get_calendar_value('select-year', this.CURRENT_YEAR);
            var month = this.get_calendar_value('select-month', new_date.getMonth() + 1);
            var date = this.get_calendar_value('select-date', new_date.getDate());

            var dateObj = new Date(year, month - 1, date);

            return dateObj;
        };

        Form.prototype.get_calendar_value = function (id, default_value) {
            var _this = this;
            var select = document.getElementById(id);

            if (id != "select-date") {
                select.onchange = function () {
                    var new_date = new Date();
                    _this.fill_dates("select-date", 1, 31, new_date.getDate());
                };
            } else {
                select.onchange = function () {
                    _this.get_date();
                };
            }

            if (select.options.length > 1) {
                return select.options[select.selectedIndex.toString()].value;
            }

            return default_value;
        };

        Form.prototype.fill_dates = function (id, min, max, today) {
            var select = document.getElementById(id);

            while (select.childNodes.length >= 1) {
                select.removeChild(select.firstChild);
            }

            if ((max > 20) && (id == "select-date")) {
                var date = this.get_date();

                var year = this.CURRENT_YEAR;
                var month = date.getMonth() + 1;

                var days = null;

                if (month == 4 || month == 6 || month == 9 || month == 11)
                    days = 30;
                else if (month == 2) {
                    //Do not forget leap years!!!
                    if (year % 400 == 0 || (year % 4 == 0 && year % 100 != 0)) {
                        days = 29;
                    } else {
                        days = 28;
                    }
                } else
                    days = 31;

                max = days;
            }

            if (today > max) {
                today = 1;
            }

            for (var i = min; i <= (max + 3); i++) {
                var newOption = document.createElement("option");
                var value = i.toString();

                if (i == today) {
                    newOption.selected = true;
                }

                if (today < 2000) {
                    value = ("0" + value).slice(-2);
                }

                if (i > max) {
                    value = "";
                }

                newOption.value = value;
                newOption.text = value;
                newOption.innerHTML = value;
                select.appendChild(newOption);
            }
        };

        // "меню" с кнопками
        Form.prototype.FormMenu = function (settings) {
            // text - выводимый сверху текст.
            // buttons - массив, каждый элемент которого - структура с полями: текст кнопки и функция,
            // вызываемая по нажатию
            // Также хорошо бы помнить, что много кнопок на экран не вмещается. От силы 5 штук.
            var _this = this;
            this.id = "form-1";

            // откроем форму и отобразим поясняющий текст
            this.open("form-1");

            this.value = ""; // !!!!

            document.getElementById("caption-1").innerHTML = "";
            document.getElementById("caption-1").style.display = "none";
            document.getElementById("text-1").innerHTML = "";
            document.getElementById("text-1").style.display = "none";
            document.getElementById("options-1").innerHTML = "";
            document.getElementById("options-1").style.display = "none";

            document.getElementById("select-calendar").style.display = "none";

            document.getElementById("form-1").style.backgroundColor = "";
            document.getElementById("form-1").className = "win ";

            if (settings.caption) {
                document.getElementById("caption-1").innerHTML = settings.caption;
                document.getElementById("caption-1").style.display = "block";
            }

            if (settings.text) {
                document.getElementById("text-1").innerHTML = settings.text;
                document.getElementById("text-1").style.display = "block";
            }

            if (settings.className) {
                document.getElementById("form-1").className += settings.className;
            }

            if (settings.backgroundColor) {
                document.getElementById("form-1").style.backgroundColor = settings.backgroundColor;
            }

            if (settings.options) {
                document.getElementById("options-1").style.display = "block";

                var all_options = document.getElementById("options-1");

                /*
                var select = (<HTMLSelectElement>document.createElement("select"));
                
                select.className = "select-1";
                
                select.style.width = '98%';
                select.size = 10;
                
                */
                var input_template = "<label class='radio-label' for='b%d'><input id='b%d' type='radio' name='chk_group' value='%d' title='%s' />%s</label>";

                var selectArr = new Array();
                selectArr.push('<div id="select-1" size=10>');

                for (var i = 0; i < settings.options.length; i++) {
                    var res = input_template;

                    res = res.replace("%d", settings.options[i]["id"]);
                    res = res.replace("%d", settings.options[i]["id"]);
                    res = res.replace("%d", settings.options[i]["id"]);

                    res = res.replace("%s", settings.options[i]["name"]);
                    res = res.replace("%s", settings.options[i]["name"]);
                    res = res.replace("%s", settings.options[i]["name"]);

                    /*res = res.replace("%s", settings.options[i]["name"]);*/
                    selectArr.push(res);
                    /*delete settings.options[i];*/
                }

                settings.options = null;

                selectArr.push("</div>");

                all_options.innerHTML = selectArr.join("");

                var select = document.getElementById("select-1");

                select.style.height = (document.body.clientHeight / 2) + "px";

                /*
                var labels = document.getElementsByClassName("radio-label");
                
                
                for (var j = 0; j < labels.length; j++) {
                
                var object = <HTMLElement> labels[i];
                
                for(var i=0;i<object.childNodes.length;i++) {
                object.childNodes[i].onclick();
                }
                }
                
                */
                var form = this;

                select.onclick = function () {
                    var radios = document.getElementsByName("chk_group");

                    for (var i = 0; i < radios.length; i++) {
                        var item = radios[i];
                        if (item.checked) {
                            ;

                            form.value = item.value;
                            form.text = item.title;

                            break;
                        }
                    }
                };

                document.getElementById("options-1").style.display = "block";
            }

            if (settings.input) {
                var all_options = document.getElementById("options-1");

                document.getElementById("options-1").style.display = "block";

                var input = document.createElement("input");

                input.className = "input-1";

                input.type = "text";

                input.style.width = '98%';

                input.className = "hugetext centered";

                input.value = "";

                input.onchange = function () {
                    _this.value = input.value;
                };

                all_options.appendChild(input);

                input.focus();
            }

            if (settings.date) {
                var today = new Date();

                var year = today.getFullYear();

                this.fill_dates("select-year", year - 2, year + 5, year);
                this.fill_dates("select-month", 1, 12, today.getMonth() + 1);
                this.fill_dates("select-date", 1, 31, today.getDate());

                var select_calendar = document.getElementById("select-calendar");

                select_calendar.style.display = "block";
            }

            //button.value = item;
            //button.onclick = settings.buttons[item];
            var all_buttons = document.getElementById("buttons-1");
            all_buttons.innerHTML = "";

            var buttons_count = 0;

            for (var item in settings.buttons) {
                var button = document.createElement("input");

                button.type = "button";
                button.className = "HugeBtn";
                button.value = item;
                button.onclick = settings.buttons[item];

                all_buttons.appendChild(button);
                buttons_count += 1;
            }

            all_buttons.className = "";

            if (buttons_count <= 2) {
                all_buttons.className = "FooterDIV2";
            }
        };

        /**
        * Форма ввода количества - 5
        *
        *
        * text - выводимый сверху текст.
        * default_value - значение по умолчанию, возвращаемое в случае отмены ввода
        * min_value - минимальное допустимое значение величины
        * max_value - максимальное допустимое значение величины
        */
        Form.prototype.FormCount = function (settings) {
            // откроем форму и отобразим поясняющий текст
            this.open("form-5");
            document.getElementById("caption-5").innerHTML = settings.text;

            var input = document.getElementById("value-5");

            input.value = "";

            if (settings.default_value) {
                input.value = settings.default_value;
            }

            /*
            * Разрешить ввод только цифр и точки
            input.onkeyup = ()=>{
            input.value = input.value.replace(/[^\d.]/,'');
            };
            */
            input.focus();

            var all_buttons = document.getElementById("buttons-5");
            all_buttons.innerHTML = "";

            // Принять
            var button = document.createElement("input");
            button.type = "button";
            button.className = "HugeBtn";
            button.value = "Принять";
            button.onclick = function () {
                settings.apply(input.value);
            };
            all_buttons.appendChild(button);

            // Отмена
            var button = document.createElement("input");
            button.type = "button";
            button.className = "HugeBtn";
            button.value = "Отмена";
            button.onclick = function () {
                settings.cancel();
            };

            all_buttons.appendChild(button);
        };
        return Form;
    })();
    FormModule.Form = Form;
})(FormModule || (FormModule = {}));
var __extends = this.__extends || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var TaskModule;
(function (TaskModule) {
    var Task = (function (_super) {
        __extends(Task, _super);
        function Task() {
            _super.call(this);
            this.BCTUSER = 1;
            this.BCTPALLET = 2;
            this.BCTCELL = 3;
            this.BCTDELIVERY = 5;
            this.BCTPARTY = 7;

            status = false; // статус - выполняется
        }
        Task.prototype.menu = function (args) {
            var form = new FormModule.Form();
            return form.FormMenu(args);
        };

        Task.prototype.formCount = function (args) {
            var form = new FormModule.Form();
            return form.FormCount(args);
        };

        Task.prototype.init = function () {
            main.init();
        };

        Task.prototype.start = function () {
        };

        Task.prototype.toogle_status = function () {
            var point = document.getElementById("point-status");
            //point.style.display = (point.style.display == "none") ? "block" : "none";
        };

        Task.prototype.task_check = function () {
            var _this = this;
            this.toogle_status();

            if (status == "false" || status == false) {
                return false;
            }

            this.ajax({
                type: "POST",
                url: "/task/check",
                hidden: true,
                success: function (resp) {
                    if ((status == "true") || (status == true)) {
                        _this.application_reload();
                    }

                    if (resp && resp["task_id"]) {
                        var task = new TaskModule.Task();

                        task.task_id = resp["task_id"];
                        task.type_id = resp["type_id"];
                        task.header_id = resp["header_id"];
                        task.description = resp["description"];

                        task.task_new();
                    }
                },
                error: function () {
                }
            });
        };

        Task.prototype.task_new = function () {
            var _this = this;
            status = false;

            this.new_event();

            this.menu({
                caption: "Новое задание",
                text: this.description,
                backgroundColor: 'lightgreen',
                buttons: {
                    "Принять задачу": function () {
                        _this.task_apply();
                    },
                    "Отменить": function () {
                        _this.task_cancel();
                    }
                }
            });
        };

        Task.prototype.task_apply = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/task/apply",
                data: { 'task_id': this.task_id },
                success: function (resp) {
                    var task;

                    switch (parseInt(_this.type_id)) {
                        case 1:
                            task = new OrderBatchingModule.OrderBatching();
                            break;
                        case 11:
                            task = new OrderBatchingModule.OrderBatching();
                            break;

                        case 3:
                            task = new AllocationModule.Allocation();
                            break;
                        case 9:
                            task = new AllocationModule.Allocation();
                            break;

                        case 5:
                            task = new AcceptanceModule.Acceptance();
                            task.message_count = "Введите число коробок на паллете";
                            break;

                        case 6:
                            task = new MovingModule.Moving();
                            break;
                        case 7:
                            task = new MovingModule.Moving();
                            break;

                        case 10:
                            task = new AcceptanceModule.Acceptance();
                            task.message_count = "Введите количество упаковок для тары или вес в кг для сырья";
                            break;

                        case 12:
                            task = new OrderBatchingRawModule.OrderBatchingRaw();
                            break;

                        case 13:
                            task = new CheckingRawModule.CheckingRaw();
                            break;
                    }

                    task.task_id = _this.task_id;
                    task.type_id = _this.type_id;
                    task.header_id = _this.header_id;
                    task.start();
                },
                error: function () {
                    main.init();
                }
            });
        };

        Task.prototype.task_cancel = function () {
            this.ajax({
                type: "POST",
                url: "/task/cancel",
                data: { 'task_id': this.task_id },
                success: function (resp) {
                    main.init();
                },
                error: function () {
                    main.init();
                }
            });
        };

        Task.prototype.stop = function (msg) {
            var _this = this;
            this.menu({
                caption: "Задание прервано",
                text: msg,
                buttons: {
                    "Прервать задачу": function () {
                        _this.abort();
                    }
                }
            });
        };

        Task.prototype.complete = function (msg) {
            var _this = this;
            this.menu({
                caption: "Задание завершено",
                text: msg,
                buttons: {
                    "Завершить задачу": function () {
                        _this.done();
                    }
                }
            });
        };

        Task.prototype.done = function () {
            if (this.task_id) {
                this.ajax({
                    type: "POST",
                    url: "/task/complete",
                    data: { 'task_id': this.task_id },
                    success: function () {
                        main.init();
                    },
                    error: function () {
                        main.init();
                    }
                });
            } else {
                main.init();
            }
        };

        Task.prototype.abort = function () {
            if (this.task_id) {
                this.ajax({
                    type: "POST",
                    url: "/task/abort",
                    data: { 'task_id': this.task_id },
                    success: function () {
                        main.init();
                    },
                    error: function () {
                        main.init();
                    }
                });
            } else {
                main.init();
            }
        };

        Task.prototype.formDelivery = function (settings) {
            settings.type = this.BCTDELIVERY;
            settings.id = "FormBarcodeUser";

            if (!settings.text) {
                settings.text = "Ввод штрих-кода сборочного";
            }

            this.formBarcode(settings);
        };

        Task.prototype.formUser = function (settings) {
            settings.type = this.BCTUSER;
            settings.id = "FormBarcodeUser";
            settings.backgroundColor = "#FF6";

            if (!settings.text) {
                settings.text = "Ввод штрих-кода пользователя";
            }

            this.formBarcode(settings);
        };

        Task.prototype.formCell = function (settings) {
            //settings.type = this.BCTCELL;
            settings.id = "FormBarcodeCell";

            if (!settings.caption) {
                settings.caption = "Ввод штрих-кода ячейки";
            }

            this.formBarcode(settings);
        };

        Task.prototype.formPallet = function (settings) {
            settings.type = this.BCTPALLET;
            settings.id = "FormBarcodePallet";

            if (!settings.text) {
                settings.text = "Ввод штрих-кода паллеты";
            }

            this.formBarcode(settings);
        };

        Task.prototype.formParty = function (settings) {
            settings.type = this.BCTPARTY;
            settings.id = "FormBarcodeParty";

            if (!settings.text) {
                settings.text = "Ввод штрих-кода партии";
            }

            this.formBarcode(settings);
        };

        Task.prototype.formBarcode = function (settings) {
            var _this = this;
            var form = new FormModule.Form();

            var callback_apply = settings.apply;
            var callback_cancel = settings.cancel;

            settings.ApplyOnScan = true;

            settings.apply = function (barcode) {
                _this.barcode.type = settings.type;
                _this.barcode.expected = settings.expected;

                if (_this.barcode.set(barcode)) {
                    callback_apply(_this.barcode.value);
                } else {
                    _this.scanner = form.scanner;
                    _this.scanner.init();
                }
            };

            settings.cancel = function () {
                if (callback_cancel) {
                    callback_cancel();
                } else {
                    _this.stop();
                }
            };

            form.FormBarcode(settings);
            /*
            form.FormBarcode({
            
            caption: settings.caption,
            backgroundColor: settings.backgroundColor,
            id:   settings.id,
            text: settings.text,
            ApplyOnScan: true,
            apply: (barcode) => {
            
            
            this.barcode.type = settings.type;
            this.barcode.expected = settings.expected;
            
            if (this.barcode.set(barcode)){
            
            settings.apply(this.barcode.value);
            }
            else{
            this.scanner = form.scanner;
            this.scanner.init();
            }
            
            },
            cancel: () => {
            if (settings.cancel){
            settings.cancel();
            }
            else{
            this.stop();
            }
            
            
            },  // возврат на начальную форму
            });
            */
        };
        return Task;
    })(CoreModule.Core);
    TaskModule.Task = Task;
})(TaskModule || (TaskModule = {}));
/// <reference path="task.ts" />
var MainModule;
(function (MainModule) {
    var Main = (function (_super) {
        __extends(Main, _super);
        function Main() {
            _super.call(this);

            var task = new TaskModule.Task();

            setInterval(function () {
                task.task_check();
            }, 2000);
        }
        Main.prototype.init = function () {
            this.user_name = "";
            this.user_depart = "";
            this.user_role = "";

            this.auth();
        };

        Main.prototype.auth = function (value) {
            var _this = this;
            if (typeof value === "undefined") { value = ""; }
            this.ajax({
                type: "POST",
                url: "/auth",
                data: ({ barcode: value }),
                success: function (resp) {
                    if (resp) {
                        _this.user_name = resp["name"];
                        _this.user_depart = resp["depart"];
                        _this.user_role = resp["role_name"];
                        _this.rc = resp["rc"];

                        _this.main();
                    } else {
                        _this.login();
                    }
                },
                error: function () {
                    _this.login();
                }
            });
        };

        Main.prototype.login = function () {
            var _this = this;
            status = false;

            this.formUser({
                apply: function (value) {
                    _this.auth(value);
                },
                cancel: function () {
                }
            });
        };

        Main.prototype.logout = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/logout",
                success: function () {
                    _this.init();
                },
                error: function () {
                    _this.init();
                }
            });
        };

        Main.prototype.main = function () {
            var _this = this;
            status = true; /* Пользователь может принимать задания */

            var form = new FormModule.Form();

            var caption = this.user_name;

            var buttons = {
                "Инвентаризация": function () {
                    var task = new InventoryModule.Inventory();
                },
                "Выход": function () {
                    _this.logout();
                }
            };

            if (this.rc == "1") {
                var rc_buttons = {
                    "Подтоварка": function () {
                        var task = new ManualIncreaseModule.ManualIncrease();
                    }
                };

                buttons = this.extend(rc_buttons, buttons);
            }

            form.FormMenu({
                caption: caption,
                text: "Выберите режим",
                buttons: buttons
            });
            /* To remove */
            /*
            var task2 = new GetCellInfoModule.GetCellInfo();
            task2.cell_id = "3000301210143";
            task2.checkCell();
            */
        };
        return Main;
    })(TaskModule.Task);
    MainModule.Main = Main;
})(MainModule || (MainModule = {}));
var InventoryModule;
(function (InventoryModule) {
    var Inventory = (function (_super) {
        __extends(Inventory, _super);
        function Inventory() {
            _super.call(this);
            this.class_name = "Inventory";
            this.all_products = [];
            this.all_party_status = [];

            this.caption = "Инвентаризация";

            this.init();
            //this.getDateValid();
        }
        Inventory.prototype.init = function () {
            var _this = this;
            var buttons = {
                "Взять из ячейки": function () {
                    var task = new GetFromCellModule.GetFromCell();
                },
                "Привязка партии": function () {
                    _this.plus = 0;
                    _this.start();
                },
                "Добавление партии": function () {
                    _this.plus = 1;
                    _this.start();
                },
                "Очистка ячейки": function () {
                    _this.emptyCell();
                },
                "Проверка ячейки": function () {
                    var task = new GetCellInfoModule.GetCellInfo();
                },
                "Перемещение ячейки": function () {
                    var task = new MovingPalletModule.MovingPallet();
                },
                "Перемещение Партии Сырья": function () {
                    var task = new MovingRawModule.MovingRaw();
                },
                "Заблокировать ячейку": function () {
                    _this.blockCell();
                },
                "Разблокировать ячейку": function () {
                    _this.unblockCell();
                }
            };

            if (main.rc == "6") {
                var msk_buttons = {
                    "Прием ГП с производства": function () {
                        _this.plus = 2;
                        _this.start();
                    },
                    "Добавление ГП с производства": function () {
                        _this.plus = 3;
                        _this.start();
                    },
                    "Отгрузка клиенту": function () {
                        var task = new OutputProductModule.OutputProduct();
                    },
                    "Приемка упаковки": function () {
                        var task = new InputProductModule.InputProduct();
                    },
                    "Списание с производства": function () {
                        var task = new ClearTovarModule.ClearTovar();
                    }
                };

                buttons = this.extend(buttons, msk_buttons);
            }

            if (main.rc == "1") {
                var rc_buttons = {
                    "Подтоварка штучной сборки": function () {
                        var task = new PodtovarkaShtukaModule.PodtovarkaShtuka();
                    },
                    "Отправка паллеты": function () {
                        _this.set_pallet_delivery();
                    },
                    "Перемещение с штучного": function () {
                        _this.send_from_item_to_delivery();
                    }
                };

                buttons = this.extend(buttons, rc_buttons);
            }

            buttons = this.extend(buttons, {
                "Назад": function () {
                    _this.stop();
                }
            });

            var form = new FormModule.Form();
            form.FormMenu({
                text: "Выберите режим",
                buttons: buttons
            });
        };

        Inventory.prototype.start = function () {
            _super.prototype.start.call(this);

            this.cell_id = "";
            this.party_id = "";
            this.pallet_id = "";

            this.product_id = "";
            this.product_code = "";
            this.product_name = "";

            this.party_number = "";

            this.count_inbox = 0;
            this.count = 0;

            if (!this.plus) {
                this.plus = 0; // Признак привязки.
            }

            this.scanCell();
        };

        Inventory.prototype.scanCell = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.scanPallet();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        Inventory.prototype.scanPallet = function () {
            var _this = this;
            this.formPallet({
                apply: function (value) {
                    _this.pallet_id = value;
                    _this.scanParty();
                },
                cancel: function () {
                    _this.scanCell();
                }
            });
        };

        Inventory.prototype.scanParty = function () {
            var _this = this;
            this.formParty({
                apply: function (value) {
                    _this.party_id = value;
                    _this.checkParty();
                },
                cancel: function () {
                    _this.scanPallet();
                }
            });
        };

        /**
        * Проверка новая партия или старая
        *
        */
        Inventory.prototype.checkParty = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/checkparty",
                data: {
                    party_id: this.party_id
                },
                success: function (resp) {
                    if (resp["is_new"]) {
                        /****
                        *  Ввод типа партии, товара, срока годности  и т.д.
                        */
                        if (!_this.product_id) {
                            _this.getCode();
                        } else {
                            _this.getCountInBox();
                        }
                    } else {
                        _this.getCount();
                    }
                },
                error: function () {
                    _this.scanParty();
                }
            });
        };

        Inventory.prototype.getCode = function () {
            var _this = this;
            var msg = "Введите код товара";

            var form = new FormModule.Form();

            form.FormCount({
                caption: this.caption,
                text: msg,
                default_value: parseInt(this.product_code),
                min_value: 1,
                apply: function (value) {
                    _this.getProduct(value);
                },
                cancel: function () {
                    _this.scanParty();
                }
            });
        };

        /**
        * Поиск продукта по базе
        *
        */
        Inventory.prototype.getProduct = function (value) {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/get_product",
                data: {
                    product_code: value
                },
                success: function (resp) {
                    if (resp.length == 1) {
                        _this.product_id = resp[0]["id"];
                        _this.product_code = resp[0]["code"];
                        _this.product_name = resp[0]["name"];
                        _this.getConfirmProduct();
                    } else {
                        _this.all_products = resp;
                        _this.showCatalog();
                    }
                },
                error: function () {
                    _this.getCode();
                }
            });
        };

        Inventory.prototype.showCatalog = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Выберите продукт",
                options: this.all_products,
                buttons: {
                    "Продолжить": function () {
                        _this.product_id = form.value;
                        _this.product_name = form.text;

                        _this.getConfirmProduct();
                    },
                    "Вернуться": function () {
                        _this.getCode();
                    }
                }
            });
        };

        /**
        * Подтвердить выбранный продукт
        *
        */
        Inventory.prototype.getConfirmProduct = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Подтверждение продукта",
                text: this.product_name,
                buttons: {
                    "Потвердить": function () {
                        _this.getCountInBox();
                    },
                    "Вернуться": function () {
                        _this.getCode();
                    }
                }
            });
        };

        /**
        *   Ввод количества товара в коробоке
        *
        */
        Inventory.prototype.getCountInBox = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormCount({
                caption: this.caption,
                text: "Введите количество товара В КОРОБКЕ (для сырья в упаковке)",
                default_value: this.count_inbox,
                apply: function (value) {
                    _this.count_inbox = value;

                    //this.getCount();
                    _this.getDateValid();
                },
                cancel: function () {
                    _this.getConfirmProduct();
                }
            });
        };

        Inventory.prototype.getDateValid = function () {
            //this.getPartyStatus();
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Введите срок годности",
                date: true,
                buttons: {
                    "Продолжить": function () {
                        _this.goden_do = form.get_timestamp();

                        //this.getPartyStatus();
                        _this.getCount();
                    },
                    "Вернуться": function () {
                        _this.getPartyNumber();
                    }
                }
            });
        };

        /**
        *   Ввод количества коробок
        *
        */
        Inventory.prototype.getCount = function () {
            //this.count = 5;
            var _this = this;
            var msg = "Введите количество КОРОБОК или всего кг для сырья";

            var form = new FormModule.Form();

            form.FormCount({
                caption: this.caption,
                text: msg,
                apply: function (value) {
                    _this.count = value;
                    _this.getPartyNumber();
                },
                cancel: function () {
                    if (_this.count_inbox) {
                        _this.getCountInBox();
                    } else {
                        _this.scanParty();
                    }
                }
            });
        };

        Inventory.prototype.getPartyNumber = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Введите обозначение партии",
                input: true,
                buttons: {
                    "Продолжить": function () {
                        _this.party_number = form.value;

                        //this.getDateValid();
                        _this.getPartyStatus();
                    },
                    "Вернуться": function () {
                        _this.getCount();
                    }
                }
            });
        };

        Inventory.prototype.getPartyStatus = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/all_party_status",
                success: function (resp) {
                    _this.all_party_status = resp;
                    _this.setPartyStatus();
                },
                error: function () {
                    _this.setParty();
                }
            });
        };

        Inventory.prototype.setPartyStatus = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Выберите статус партии",
                options: this.all_party_status,
                buttons: {
                    "Выбрать": function () {
                        _this.party_status = form.value;

                        _this.setParty();
                    },
                    "Пропустить": function () {
                        _this.setParty();
                    }
                }
            });
        };

        Inventory.prototype.setParty = function () {
            /*
            pPallet in integer,
            pParty in integer,
            pTovar in integer,
            pInBox in integer,
            pDataDo in date,
            pNum varchar2,
            pCell in integer,
            pVal in float,
            pPlus in integer,
            pRet out varchar2
            */
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/setparty",
                data: {
                    cell_id: this.cell_id,
                    pallet_id: this.pallet_id,
                    party_id: this.party_id,
                    product_id: this.product_id,
                    party_number: this.party_number,
                    party_status: this.party_status,
                    count_inbox: this.count_inbox,
                    count: this.count,
                    plus: this.plus,
                    goden_do: this.goden_do
                },
                success: function () {
                    _this.chooseType();
                },
                error: function () {
                    _this.getCount();
                }
            });
        };

        Inventory.prototype.chooseType = function () {
            var _this = this;
            var msg = "Ячейка: " + this.cell_id;

            var form = new FormModule.Form();

            form.FormMenu({
                text: msg,
                buttons: {
                    "Добавить такой же товар": function () {
                        _this.count = 0;
                        _this.count_inbox = 0;

                        _this.plus = 1;
                        _this.scanParty();
                    },
                    "Добавить ДРУГОЙ товар": function () {
                        _this.product_id = "";
                        _this.product_code = "";
                        _this.product_name = "";

                        _this.count = 0;
                        _this.count_inbox = 0;

                        _this.plus = 1;
                        _this.scanParty();
                    },
                    "Завершить задачу": function () {
                        _this.complete();
                    }
                }
            });
        };

        /**
        *   Очистка ячейки
        */
        Inventory.prototype.emptyCell = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.setEmptyCell();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        Inventory.prototype.setEmptyCell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/empty_cell",
                data: {
                    cell_id: this.cell_id
                },
                success: function () {
                    _this.complete("Ячейка очищена");
                },
                error: function () {
                    _this.emptyCell();
                }
            });
        };

        Inventory.prototype.blockCell = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.setBlockCell();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        Inventory.prototype.setBlockCell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/block_cell",
                data: {
                    cell_id: this.cell_id
                },
                success: function () {
                    _this.complete("Ячейка заблокирована");
                },
                error: function () {
                    _this.blockCell();
                }
            });
        };

        Inventory.prototype.unblockCell = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.setUnblockCell();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        Inventory.prototype.setUnblockCell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/unblock_cell",
                data: {
                    cell_id: this.cell_id
                },
                success: function () {
                    _this.complete("Ячейка разблокирована");
                },
                error: function () {
                    _this.blockCell();
                }
            });
        };

        Inventory.prototype.set_pallet_delivery = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.send_to_client();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        Inventory.prototype.send_to_client = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/set_pallet_delivery",
                data: {
                    cell_id: this.cell_id
                },
                success: function () {
                    _this.complete("Паллета Отправлена успешно");
                },
                error: function () {
                    _this.stop();
                }
            });
        };

        Inventory.prototype.send_from_item_to_delivery = function () {
            var _this = this;
            this.formDelivery({
                apply: function (value) {
                    _this.delivery_id = value;
                    _this.send_to_delivery();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        Inventory.prototype.send_to_delivery = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/send_from_item_to_delivery",
                data: {
                    delivery_id: this.delivery_id
                },
                success: function (resp) {
                    var msg = "Взять из ячейки: " + resp.cell_name + "      коробок: " + resp.count;
                    _this.complete(msg);
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return Inventory;
    })(TaskModule.Task);
    InventoryModule.Inventory = Inventory;
})(InventoryModule || (InventoryModule = {}));
/// <reference path="../inventory/inventory.ts" />
var CheckingRawModule;
(function (CheckingRawModule) {
    var CheckingRaw = (function (_super) {
        __extends(CheckingRaw, _super);
        function CheckingRaw() {
            _super.call(this);
            this.class_name = "CheckingRaw";

            this.caption = "Проверка сборки заказа по сырью";
            this.party_id = "";
        }
        CheckingRaw.prototype.scanParty = function () {
            var _this = this;
            this.formParty({
                text: "Ввод экстра-партии",
                apply: function (value) {
                    _this.party_id = value;
                    _this.ScanExtraParty_Raw();
                },
                cancel: function () {
                    _this.scanPallet();
                }
            });
        };

        CheckingRaw.prototype.ScanExtraParty_Raw = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/sborka/scan_extra_party_raw",
                data: {
                    party_id: this.party_id,
                    header_id: this.header_id
                },
                success: function (resp) {
                    if (parseInt(resp.count) == 0) {
                        _this.IsRawHeaderReady();
                    } else {
                        _this.scanParty();
                    }
                },
                error: function () {
                    _this.scanParty();
                }
            });
        };

        CheckingRaw.prototype.IsRawHeaderReady = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/sborka/is_raw_header_ready",
                data: {
                    header_id: this.header_id
                },
                success: function (resp) {
                    _this.complete("Заказ проверен");
                },
                error: function () {
                    _this.scanParty();
                }
            });
        };

        CheckingRaw.prototype.get_mode = function () {
            var _this = this;
            this.menu({
                caption: "Выберите режим",
                buttons: {
                    "Взять ещё с ячейки": function () {
                        _this.party_id = "";
                        _this.count = 0;
                        _this.scanParty();
                    },
                    "Завершить подтоварку": function () {
                        _this.end_factura();
                    }
                }
            });
        };

        CheckingRaw.prototype.end_factura = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/sborka/end_factura_for_shtuka",
                data: {
                    header_id: this.header_id
                },
                success: function () {
                    _this.complete();
                }
            });
        };
        return CheckingRaw;
    })(InventoryModule.Inventory);
    CheckingRawModule.CheckingRaw = CheckingRaw;
})(CheckingRawModule || (CheckingRawModule = {}));
/// <reference path="../inventory/inventory.ts" />
var PodtovarkaShtukaModule;
(function (PodtovarkaShtukaModule) {
    var PodtovarkaShtuka = (function (_super) {
        __extends(PodtovarkaShtuka, _super);
        function PodtovarkaShtuka() {
            _super.call(this);
            this.class_name = "PodtovarkaShtuka";

            this.caption = "Подтоварка штучной сборки";
            this.cell_id = "";
            this.party_id = "";
            this.pallet_id = "";
            this.header_id = "";
            this.count = 0;

            this.get_header();
        }
        PodtovarkaShtuka.prototype.get_header = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/sborka/new_sborka_for_shtuka",
                data: {},
                success: function (resp) {
                    _this.header_id = resp.header_id;

                    _this.scanCell();
                }
            });
        };

        PodtovarkaShtuka.prototype.scanCell = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.scanPallet();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        PodtovarkaShtuka.prototype.scanPallet = function () {
            var _this = this;
            this.formPallet({
                apply: function (value) {
                    _this.pallet_id = value;
                    _this.scanParty();
                },
                cancel: function () {
                    _this.scanCell();
                }
            });
        };

        PodtovarkaShtuka.prototype.scanParty = function () {
            var _this = this;
            this.formParty({
                apply: function (value) {
                    _this.party_id = value;
                    _this.getCount();
                },
                cancel: function () {
                    _this.scanPallet();
                }
            });
        };

        /**
        *   Ввод количества коробок
        *
        */
        PodtovarkaShtuka.prototype.getCount = function () {
            var _this = this;
            var msg = "Введите количество КОРОБОК";

            var form = new FormModule.Form();

            form.FormCount({
                caption: this.caption,
                text: msg,
                default_value: this.count,
                min_value: 0,
                max_value: 1000,
                apply: function (value) {
                    _this.count = value;
                    _this.add_box();
                },
                cancel: function () {
                    _this.scanParty();
                }
            });
        };

        PodtovarkaShtuka.prototype.add_box = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/sborka/add_factura_for_shtuka",
                data: {
                    cell_id: this.cell_id,
                    party_id: this.party_id,
                    pallet_id: this.pallet_id,
                    header_id: this.header_id,
                    count: this.count
                },
                success: function () {
                    _this.get_mode();
                }
            });
        };

        PodtovarkaShtuka.prototype.get_mode = function () {
            var _this = this;
            this.menu({
                caption: "Выберите режим",
                buttons: {
                    "Взять ещё с ячейки": function () {
                        _this.party_id = "";
                        _this.count = 0;
                        _this.scanParty();
                    },
                    "Завершить подтоварку": function () {
                        _this.end_factura();
                    }
                }
            });
        };

        PodtovarkaShtuka.prototype.end_factura = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/sborka/end_factura_for_shtuka",
                data: {
                    header_id: this.header_id
                },
                success: function () {
                    _this.complete();
                }
            });
        };
        return PodtovarkaShtuka;
    })(InventoryModule.Inventory);
    PodtovarkaShtukaModule.PodtovarkaShtuka = PodtovarkaShtuka;
})(PodtovarkaShtukaModule || (PodtovarkaShtukaModule = {}));
/// <reference path="inventory.ts" />
var ClearTovarModule;
(function (ClearTovarModule) {
    var ClearTovar = (function (_super) {
        __extends(ClearTovar, _super);
        function ClearTovar() {
            _super.call(this);
            this.class_name = "ClearTovar";

            this.caption = "Списание с производства";

            this.getCode();
        }
        ClearTovar.prototype.getCountInBox = function () {
            var _this = this;
            this.menu({
                caption: "Выберите режим",
                buttons: {
                    "Списать все": function () {
                        _this.clear_tovar();
                    },
                    "Указать количество": function () {
                        _this.get_count();
                    },
                    "Отменить": function () {
                        _this.stop();
                    }
                }
            });
        };

        ClearTovar.prototype.get_count = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormCount({
                text: "Введите количество штук",
                default_value: this.count_inbox,
                apply: function (value) {
                    _this.count_inbox = value;
                    _this.clear_tovar();
                },
                cancel: function () {
                    _this.getCountInBox();
                }
            });
        };

        ClearTovar.prototype.clear_tovar = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/clear_tovar",
                data: {
                    product_id: this.product_id,
                    count_inbox: this.count_inbox
                },
                success: function () {
                    _this.complete("Товар списан с производства");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return ClearTovar;
    })(InventoryModule.Inventory);
    ClearTovarModule.ClearTovar = ClearTovar;
})(ClearTovarModule || (ClearTovarModule = {}));
/// <reference path="inventory.ts" />
var GetCellInfoModule;
(function (GetCellInfoModule) {
    var GetCellInfo = (function (_super) {
        __extends(GetCellInfo, _super);
        function GetCellInfo() {
            _super.call(this);
            this.class_name = "GetCellInfo";

            this.caption = "Проверка ячейки";

            this.cell_id = "";

            this.count = 0;

            this.scanCell();
        }
        GetCellInfo.prototype.scanCell = function () {
            var _this = this;
            /*67*/
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.checkCell();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        GetCellInfo.prototype.checkCell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/get_cell_info",
                data: {
                    cell_id: this.cell_id
                },
                success: function (resp) {
                    _this.all_cells = resp;

                    _this.count = resp.length - 1;

                    _this.show_page(0);
                },
                error: function () {
                    _this.scanCell();
                }
            });
        };

        GetCellInfo.prototype.show_page = function (page) {
            var _this = this;
            var value = this.all_cells[page];

            var text = value["tname"] + "</br>Коробок:  " + value["valume"] + "</br>В коробке:  " + value["inbox"] + "</br>Ожид. расход (в коробках): " + value["future_exps"] + "</br>Годен до:  " + value["data"] + "</br>Партия:  " + value["num"];

            var buttons = {
                "Отменить": function () {
                    _this.scanCell();
                }
            };

            var add_buttons;

            if (page > 0) {
                add_buttons = {
                    "Назад": function () {
                        _this.show_page(page - 1);
                    }
                };

                buttons = this.extend(add_buttons, buttons);
            }

            if (page < this.count) {
                add_buttons = {
                    "Вперед": function () {
                        _this.show_page(page + 1);
                    }
                };

                buttons = this.extend(add_buttons, buttons);
            }

            var caption = value["name"] + "  (" + (page + 1) + "/" + (this.count + 1) + ")";

            this.menu({
                caption: caption,
                text: text,
                buttons: buttons
            });
        };
        return GetCellInfo;
    })(InventoryModule.Inventory);
    GetCellInfoModule.GetCellInfo = GetCellInfo;
})(GetCellInfoModule || (GetCellInfoModule = {}));
/// <reference path="inventory.ts" />
var GetFromCellModule;
(function (GetFromCellModule) {
    var GetFromCell = (function (_super) {
        __extends(GetFromCell, _super);
        function GetFromCell() {
            _super.call(this);
            this.class_name = "GetFromCell";

            this.caption = "Взять из ячейки";

            this.cell_id = "";
            this.party_id = "";
            this.pallet_id = "";

            this.count = 0;

            this.scanCell();
            //this.set_party();
        }
        GetFromCell.prototype.scanCell = function () {
            var _this = this;
            /*67*/
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.scanPallet();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        GetFromCell.prototype.scanPallet = function () {
            var _this = this;
            this.formPallet({
                apply: function (value) {
                    _this.pallet_id = value;
                    _this.scanParty();
                },
                cancel: function () {
                    _this.scanCell();
                }
            });
        };

        GetFromCell.prototype.scanParty = function () {
            var _this = this;
            this.formParty({
                apply: function (value) {
                    _this.party_id = value;
                    _this.getCount();
                },
                cancel: function () {
                    _this.scanPallet();
                }
            });
        };

        /**
        *   Ввод количества коробок
        *
        */
        GetFromCell.prototype.getCount = function () {
            var _this = this;
            var msg = "Введите количество КОРОБОК";

            var form = new FormModule.Form();

            form.FormCount({
                caption: this.caption,
                text: msg,
                default_value: this.count,
                min_value: 0,
                max_value: 1000,
                apply: function (value) {
                    _this.count = value;
                    _this.get_target();
                },
                cancel: function () {
                    _this.scanParty();
                }
            });
        };

        GetFromCell.prototype.get_target = function () {
            var _this = this;
            var msg = "Ячейка назначения не выбрана";

            if (this.target_id) {
                msg = "Ячейка назначения: " + this.target_id;
            }

            this.menu({
                text: msg,
                buttons: {
                    "Выбрать ячейку назначения": function () {
                        _this.scan_target();
                    },
                    "Изьять из ячейки": function () {
                        _this.set_party();
                    },
                    "Назад": function () {
                        _this.getCount();
                    }
                }
            });
        };

        GetFromCell.prototype.scan_target = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.target_id = value;
                    _this.set_party();
                },
                cancel: function () {
                    _this.set_party();
                }
            });
        };

        GetFromCell.prototype.set_party = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/get_from_cell",
                data: {
                    cell_id: this.cell_id,
                    party_id: this.party_id,
                    pallet_id: this.pallet_id,
                    target_id: this.target_id,
                    count: this.count
                },
                success: function () {
                    _this.get_mode();
                },
                error: function () {
                    _this.get_mode();
                }
            });
        };

        GetFromCell.prototype.get_mode = function () {
            var _this = this;
            this.menu({
                caption: "Выберите режим",
                buttons: {
                    "Взять ещё с ячейки": function () {
                        _this.party_id = "";
                        _this.count = 0;
                        _this.scanParty();
                    },
                    "Завершить задачу": function () {
                        _this.complete();
                    }
                }
            });
        };
        return GetFromCell;
    })(InventoryModule.Inventory);
    GetFromCellModule.GetFromCell = GetFromCell;
})(GetFromCellModule || (GetFromCellModule = {}));
/// <reference path="inventory.ts" />
var InputProductModule;
(function (InputProductModule) {
    var InputProduct = (function (_super) {
        __extends(InputProduct, _super);
        function InputProduct() {
            _super.call(this);
            this.class_name = "InputProduct";

            this.caption = "Приемка упаковки";
            this.cell_id = "";
            this.header_id = "";

            this.plus = 0;

            this.startInput();
        }
        InputProduct.prototype.startInput = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/start_input",
                data: {},
                success: function (resp) {
                    _this.header_id = resp["header_id"];
                    _this.start();
                },
                error: function () {
                    _this.stop();
                }
            });
        };

        InputProduct.prototype.setParty = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/add_product_to_input",
                data: {
                    header_id: this.header_id,
                    cell_id: this.cell_id,
                    pallet_id: this.pallet_id,
                    party_id: this.party_id,
                    product_id: this.product_id,
                    party_number: this.party_number,
                    party_status: this.party_status,
                    count_inbox: this.count_inbox,
                    count: this.count,
                    plus: this.plus,
                    goden_do: this.goden_do
                },
                success: function () {
                    _this.chooseType();
                },
                error: function () {
                    _this.getCount();
                }
            });
        };

        InputProduct.prototype.chooseType = function () {
            var _this = this;
            var msg = "Ячейка: " + this.cell_id;

            var form = new FormModule.Form();

            form.FormMenu({
                text: msg,
                buttons: {
                    "Добавить такой же товар": function () {
                        _this.count = 0;
                        _this.count_inbox = 0;

                        _this.plus = 1;
                        _this.scanCell();
                    },
                    "Добавить ДРУГОЙ товар": function () {
                        _this.product_id = "";
                        _this.product_code = "";
                        _this.product_name = "";

                        _this.count = 0;
                        _this.count_inbox = 0;

                        _this.plus = 0;
                        _this.scanCell(); // Party ???
                    },
                    "Приостановить приёмку": function () {
                        _this.stop();
                    },
                    "Завершить приемку": function () {
                        _this.endInput();
                    }
                }
            });
        };

        InputProduct.prototype.endInput = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/end_input",
                data: {
                    "header_id": this.header_id
                },
                success: function () {
                    _this.complete("Приемка завершена");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return InputProduct;
    })(InventoryModule.Inventory);
    InputProductModule.InputProduct = InputProduct;
})(InputProductModule || (InputProductModule = {}));
/// <reference path="inventory.ts" />
var ManualIncreaseModule;
(function (ManualIncreaseModule) {
    var ManualIncrease = (function (_super) {
        __extends(ManualIncrease, _super);
        function ManualIncrease() {
            _super.call(this);
            this.class_name = "ManualIncrease";

            this.caption = "Ручная подтоварка";
            this.cell_id = "";
            this.scanCell();
        }
        ManualIncrease.prototype.scanCell = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.addCell();
                },
                cancel: function () {
                    _this.completeIncrease();
                }
            });
        };

        ManualIncrease.prototype.addCell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/increase/add",
                data: {
                    cell_id: this.cell_id
                },
                success: function () {
                    _this.nextCell();
                },
                error: function () {
                    _this.completeIncrease();
                }
            });
        };

        ManualIncrease.prototype.nextCell = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: this.caption,
                buttons: {
                    "Продолжить": function () {
                        _this.scanCell();
                    },
                    "Закончить подтоварку": function () {
                        _this.completeIncrease();
                    }
                }
            });
        };

        ManualIncrease.prototype.completeIncrease = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/increase/complete",
                success: function () {
                    _this.complete("Подтоварка завершена");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return ManualIncrease;
    })(InventoryModule.Inventory);
    ManualIncreaseModule.ManualIncrease = ManualIncrease;
})(ManualIncreaseModule || (ManualIncreaseModule = {}));
/// <reference path="inventory.ts" />
var MovingPalletModule;
(function (MovingPalletModule) {
    var MovingPallet = (function (_super) {
        __extends(MovingPallet, _super);
        function MovingPallet() {
            _super.call(this);
            this.class_name = "MovingPallet";

            this.caption = "Перемещение ячейки";

            this.cell_id = "";
            this.target_id = "";

            this.scanCell();
        }
        MovingPallet.prototype.scanCell = function () {
            var _this = this;
            this.formCell({
                text: "Ввод штрих-кода ИСХОДНОЙ ячейки",
                apply: function (value) {
                    _this.cell_id = value;
                    _this.destCell();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        MovingPallet.prototype.destCell = function () {
            var _this = this;
            this.formCell({
                text: "Ввод штрих-кода КОНЕЧНОЙ ячейки",
                apply: function (value) {
                    _this.target_id = value;
                    _this.setCell();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        MovingPallet.prototype.setCell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/moving/moved",
                data: {
                    'cell_id': this.cell_id,
                    'target_id': this.target_id
                },
                success: function () {
                    _this.complete("Паллета перемещена");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return MovingPallet;
    })(InventoryModule.Inventory);
    MovingPalletModule.MovingPallet = MovingPallet;
})(MovingPalletModule || (MovingPalletModule = {}));
/// <reference path="inventory.ts" />
var MovingRawModule;
(function (MovingRawModule) {
    var MovingRaw = (function (_super) {
        __extends(MovingRaw, _super);
        function MovingRaw() {
            _super.call(this);
            this.class_name = "MovingRaw";

            this.caption = "Перемещение сырья";

            this.cell_id = "";
            this.target_id = "";

            this.scanCell();
        }
        MovingRaw.prototype.scanCell = function () {
            var _this = this;
            this.formCell({
                text: "Ввод штрих-кода ИСХОДНОЙ ячейки",
                apply: function (value) {
                    _this.cell_id = value;
                    _this.scanParty();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        MovingRaw.prototype.scanParty = function () {
            var _this = this;
            this.formParty({
                apply: function (value) {
                    _this.party_id = value;
                    _this.getCell();
                },
                cancel: function () {
                    _this.scanCell();
                }
            });
        };

        MovingRaw.prototype.getCell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/moving/GetCellForPartyFromBox",
                data: {
                    'party_id': this.party_id,
                    'value': "31"
                },
                success: function (resp) {
                    _this.code = resp.code;
                    _this.complete("Паллета перемещена");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return MovingRaw;
    })(InventoryModule.Inventory);
    MovingRawModule.MovingRaw = MovingRaw;
})(MovingRawModule || (MovingRawModule = {}));
/// <reference path="inventory.ts" />
var OutputProductModule;
(function (OutputProductModule) {
    var OutputProduct = (function (_super) {
        __extends(OutputProduct, _super);
        function OutputProduct() {
            _super.call(this);
            this.class_name = "OutputProduct";

            this.caption = "Отгрузка клиенту";
            this.cell_id = "";
            this.header_id = "";

            this.allClients();
        }
        OutputProduct.prototype.allClients = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/all_clients",
                data: {},
                success: function (resp) {
                    _this.all_clients = resp;
                    _this.chooseClient();
                },
                error: function () {
                    _this.stop();
                }
            });
        };

        OutputProduct.prototype.chooseClient = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Выберите клиента",
                options: this.all_clients,
                buttons: {
                    "Продолжить": function () {
                        _this.client_id = form.value;
                        _this.client_name = form.text;

                        _this.getConfirmClient();
                    },
                    "Вернуться": function () {
                        _this.stop();
                    }
                }
            });
        };

        OutputProduct.prototype.getConfirmClient = function () {
            var _this = this;
            this.menu({
                caption: "Подтверждение клиента",
                text: this.client_name,
                buttons: {
                    "Потвердить": function () {
                        _this.startOutput();
                    },
                    "Вернуться": function () {
                        _this.allClients();
                    }
                }
            });
        };

        OutputProduct.prototype.startOutput = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/start_output",
                data: {
                    "client_id": this.client_id
                },
                success: function (resp) {
                    _this.header_id = resp["header_id"];
                    _this.scan_cell();
                },
                error: function () {
                    _this.stop();
                }
            });
        };

        OutputProduct.prototype.scan_cell = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;

                    _this.check_party();
                },
                cancel: function () {
                    _this.chooseType();
                }
            });
        };

        OutputProduct.prototype.check_party = function () {
            var _this = this;
            this.menu({
                caption: "Отгрузка клиенту",
                buttons: {
                    "Подтвердить": function () {
                        _this.addProduct();
                    },
                    "Указать партию": function () {
                        _this.scan_party();
                    },
                    "Назад": function () {
                        _this.scan_cell();
                    }
                }
            });
        };

        OutputProduct.prototype.scan_party = function () {
            var _this = this;
            this.formParty({
                apply: function (value) {
                    _this.party_id = value;
                    _this.get_count();
                },
                cancel: function () {
                    _this.check_party();
                }
            });
        };

        /**
        *   Ввод количества коробок
        *
        */
        OutputProduct.prototype.get_count = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormCount({
                text: "Введите количество КОРОБОК",
                apply: function (value) {
                    _this.count = value;
                    _this.addProduct();
                },
                cancel: function () {
                    _this.scan_party();
                }
            });
        };

        OutputProduct.prototype.addProduct = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/add_product",
                data: {
                    "count": this.count,
                    "cell_id": this.cell_id,
                    "party_id": this.party_id,
                    "header_id": this.header_id
                },
                success: function () {
                    _this.chooseType();
                },
                error: function () {
                    _this.chooseType();
                }
            });
        };

        OutputProduct.prototype.chooseType = function () {
            var _this = this;
            this.menu({
                caption: "Отгрузка клиенту",
                buttons: {
                    "Отгрузить ещё": function () {
                        _this.scan_cell();
                    },
                    "Приостановить отгрузку": function () {
                        _this.stop();
                    },
                    "Завершить": function () {
                        _this.endOutput();
                    }
                }
            });
        };

        OutputProduct.prototype.endOutput = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/inventory/end_output",
                data: {
                    "header_id": this.header_id
                },
                success: function () {
                    _this.complete("Отгрузка завершена");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return OutputProduct;
    })(InventoryModule.Inventory);
    OutputProductModule.OutputProduct = OutputProduct;
})(OutputProductModule || (OutputProductModule = {}));
var AcceptanceModule;
(function (AcceptanceModule) {
    var Acceptance = (function (_super) {
        __extends(Acceptance, _super);
        function Acceptance() {
            _super.apply(this, arguments);
            this.class_name = "Acceptance";
        }
        Acceptance.prototype.start = function () {
            _super.prototype.start.call(this);

            this.is_btk = 0;
            this.is_party_new = true;

            this.count_input = "0";
            this.count_total = "?";

            this.get_type();

            this.date_from = "";
            this.box = "1";
            this.months = "0";
            //this.get_all_products();
        };

        Acceptance.prototype.get_type = function () {
            var _this = this;
            this.caption = "Принято " + this.count_input + " штук из " + this.count_total;

            this.menu({
                caption: this.caption,
                buttons: {
                    "Принять паллету на склад": function () {
                        _this.is_btk = 0;
                        _this.get_count_total();
                    },
                    "Принять паллету в БТК": function () {
                        _this.is_btk = 1;
                        _this.get_count_total();
                    },
                    "Отменить паллету": function () {
                        _this.rollout_pallet();
                    },
                    "Завершить приемку": function () {
                        _this.end_header();
                    }
                }
            });
        };

        Acceptance.prototype.rollout_pallet = function () {
            var _this = this;
            this.formPallet({
                text: "Ввод штрих-кода паллеты для отмены",
                apply: function (value) {
                    _this.pallet_id = value;
                    _this.drop_pallet();
                },
                cancel: function () {
                    _this.get_type();
                }
            });
        };

        //  проверка приёмочной ячейки - можно ли в неё принимать
        Acceptance.prototype.drop_pallet = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/drop_pallet",
                data: {
                    pallet_id: this.pallet_id
                },
                success: function () {
                    _this.is_rollout_pallet = true;
                    _this.get_count_total();
                },
                error: function () {
                    _this.get_type();
                }
            });
        };

        Acceptance.prototype.get_count_total = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/get_count_total",
                data: {
                    header_id: this.header_id
                },
                success: function (resp) {
                    _this.count_input = resp.count_input;
                    _this.count_total = resp.count_total;

                    _this.caption = "Принято " + _this.count_input + " штук из " + _this.count_total;

                    if (_this.is_rollout_pallet) {
                        delete _this.is_rollout_pallet;
                        _this.get_type();
                    }

                    if (_this.is_btk != 1) {
                        /*
                        *  Удалять чтобы при приемке в БТК спрашивать ячейку и паллету только один раз
                        */
                        delete _this.cell_id;
                        delete _this.pallet_id;
                    }

                    if (_this.cell_id && _this.pallet_id) {
                        _this.scan_party();
                    } else {
                        _this.scan_cell();
                    }
                },
                error: function () {
                    _this.stop();
                }
            });
        };

        Acceptance.prototype.scan_cell = function () {
            var _this = this;
            this.formCell({
                caption: this.caption,
                text: "Ввод штрих-кода ячейки приёмки",
                apply: function (value) {
                    _this.cell_id = value;
                    _this.check_cell();
                },
                cancel: function () {
                    _this.get_type();
                }
            });
        };

        //  проверка приёмочной ячейки - можно ли в неё принимать
        Acceptance.prototype.check_cell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/check_cell",
                data: {
                    cell_id: this.cell_id,
                    header_id: this.header_id
                },
                success: function () {
                    _this.scan_pallet();
                },
                error: function () {
                    _this.scan_cell();
                }
            });
        };

        Acceptance.prototype.scan_pallet = function () {
            var _this = this;
            this.formPallet({
                apply: function (value) {
                    _this.pallet_id = value;
                    _this.check_pallet();
                },
                cancel: function () {
                    _this.scan_cell();
                }
            });
        };

        Acceptance.prototype.check_pallet = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/check_pallet",
                data: {
                    pallet_id: this.pallet_id,
                    header_id: this.header_id
                },
                success: function () {
                    _this.scan_party();
                },
                error: function () {
                    _this.scan_cell();
                }
            });
        };

        Acceptance.prototype.scan_party = function () {
            var _this = this;
            this.formParty({
                apply: function (value) {
                    _this.party_id = value;
                    _this.check_party();
                },
                cancel: function () {
                    _this.get_type();
                }
            });
        };

        Acceptance.prototype.check_party = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/check_party",
                data: {
                    party_id: this.party_id,
                    header_id: this.header_id
                },
                success: function (resp) {
                    if (resp["count_inbox"]) {
                        _this.count_inbox = resp["count_inbox"];
                        _this.is_party_new = false;

                        _this.get_count();
                    } else if (_this.is_btk == 1) {
                        _this.stop("Приёмка новой партии невозможна в режиме БТК");
                    } else {
                        _this.get_all_products();
                    }
                },
                error: function () {
                    _this.scan_party();
                }
            });
        };

        Acceptance.prototype.get_all_products = function () {
            //this.stop("Выбор новой партии не релизован, обратитесь к разработчикам");
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/get_all_products",
                data: {
                    header_id: this.header_id
                },
                success: function (resp) {
                    _this.all_products = resp;
                    _this.showCatalog();
                },
                error: function () {
                    _this.stop();
                }
            });
        };

        Acceptance.prototype.showCatalog = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Выберите продукт",
                options: this.all_products,
                buttons: {
                    "Продолжить": function () {
                        _this.product_id = form.value;
                        _this.product_name = form.text;

                        _this.getConfirmProduct();
                    },
                    "Вернуться": function () {
                        _this.check_party();
                    }
                }
            });
        };

        /**
        * Подтвердить выбранный продукт
        *
        */
        Acceptance.prototype.getConfirmProduct = function () {
            var _this = this;
            this.menu({
                caption: "Подтверждение продукта",
                text: this.product_name,
                buttons: {
                    "Потвердить": function () {
                        _this.getPartyNumber();
                    },
                    "Вернуться": function () {
                        _this.showCatalog();
                    }
                }
            });
        };

        Acceptance.prototype.getPartyNumber = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Введите обозначение партии",
                input: true,
                buttons: {
                    "Продолжить": function () {
                        _this.party_number = form.value;

                        _this.getDateValid();
                    },
                    "Вернуться": function () {
                        _this.getConfirmProduct();
                    }
                }
            });
        };

        Acceptance.prototype.getDateValid = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Введите срок годности",
                date: true,
                buttons: {
                    "Продолжить": function () {
                        _this.goden_do = form.get_timestamp();

                        _this.getCountInBox();
                    },
                    "Вернуться": function () {
                        _this.getPartyNumber();
                    }
                }
            });
        };

        /**** Для сырья  ****/
        Acceptance.prototype.get_date_from = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Введите дату производства",
                date: true,
                buttons: {
                    "Продолжить": function () {
                        _this.date_from = form.get_timestamp();

                        _this.get_months();
                    },
                    "Вернуться": function () {
                        _this.getDateValid();
                    }
                }
            });
        };

        Acceptance.prototype.get_months = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Введите кол-во месяцев годен",
                input: true,
                buttons: {
                    "Продолжить": function () {
                        _this.months = form.value;

                        _this.get_box();
                    },
                    "Вернуться": function () {
                        _this.get_date_from();
                    }
                }
            });
        };

        Acceptance.prototype.get_box = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Введите кол-во мест на паллете",
                input: true,
                buttons: {
                    "Продолжить": function () {
                        _this.box = form.value;

                        _this.get_count();
                    },
                    "Вернуться": function () {
                        _this.get_months();
                    }
                }
            });
        };

        /**
        *   Ввод количества товара в коробоке
        *
        */
        Acceptance.prototype.getCountInBox = function () {
            var _this = this;
            /*
            * Если принимаем сырье, то не спрашивать количество в упаковке, а отправлять 1
            */
            if (parseInt(this.type_id) == 10) {
                this.count_inbox = "1";

                this.get_date_from();

                //this.get_count();
                return true;
            }

            var form = new FormModule.Form();

            form.FormCount({
                text: "Введите количество в упаковке",
                default_value: this.count_inbox,
                apply: function (value) {
                    _this.count_inbox = value;
                    _this.get_count();
                },
                cancel: function () {
                    _this.getDateValid();
                }
            });
        };

        Acceptance.prototype.get_count = function () {
            var _this = this;
            this.formCount({
                text: this.message_count,
                apply: function (value) {
                    _this.count = value;

                    if (_this.is_btk) {
                        // переход на форму ввода общего числа штук
                        _this.get_count_all();
                    } else if (_this.is_party_new) {
                        //this.stop("Ввод количества для новой партии закрыт, обратитесь к разработчикам");
                        delete _this.count_all;

                        _this.addnewpallet();
                    } else {
                        // Старая партия
                        // переход на приемку след. паллеты - на форму ввода ШК ячейки
                        delete _this.count_all;
                        _this.addnewpallet_oldparty();
                    }
                },
                cancel: function () {
                    _this.getCountInBox();
                }
            });
        };

        Acceptance.prototype.get_count_all = function () {
            var _this = this;
            this.formCount({
                caption: "Режим БТК",
                text: "Введите общее количество штук",
                apply: function (value) {
                    _this.count_all = value;
                    _this.addnewpallet_oldparty();
                },
                cancel: function () {
                    _this.get_type();
                }
            });
        };

        Acceptance.prototype.addnewpallet = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/addnewpallet",
                data: {
                    header_id: this.header_id,
                    pallet_id: this.pallet_id,
                    party_id: this.party_id,
                    cell_id: this.cell_id,
                    count: this.count,
                    is_btk: this.is_btk,
                    count_inbox: this.count_inbox,
                    product_id: this.product_id,
                    party_number: this.party_number,
                    goden_do: this.goden_do,
                    /*   Для сырья  */
                    date_from: this.date_from,
                    box: this.box,
                    months: this.months
                },
                success: function () {
                    _this.get_count_total();
                },
                error: function () {
                    _this.get_count();
                }
            });
        };

        Acceptance.prototype.addnewpallet_oldparty = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/addnewpallet_oldparty",
                data: {
                    header_id: this.header_id,
                    pallet_id: this.pallet_id,
                    party_id: this.party_id,
                    cell_id: this.cell_id,
                    count: this.count,
                    is_btk: this.is_btk,
                    count_all: this.count_all
                },
                success: function () {
                    _this.get_count_total();
                },
                error: function () {
                    _this.get_count();
                }
            });
        };

        Acceptance.prototype.end_header = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/acception/end_header",
                data: {
                    header_id: this.header_id
                },
                success: function () {
                    _this.complete("Приемка завершена");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return Acceptance;
    })(TaskModule.Task);
    AcceptanceModule.Acceptance = Acceptance;
})(AcceptanceModule || (AcceptanceModule = {}));
var AllocationModule;
(function (AllocationModule) {
    var Allocation = (function (_super) {
        __extends(Allocation, _super);
        function Allocation() {
            _super.apply(this, arguments);
            this.class_name = "Allocation";
        }
        Allocation.prototype.start = function () {
            _super.prototype.start.call(this);

            this.scan_pallet();
        };

        Allocation.prototype.scan_pallet = function () {
            var _this = this;
            this.formPallet({
                apply: function (value) {
                    _this.pallet_id = value;
                    _this.scan_cell();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        Allocation.prototype.scan_cell = function () {
            var _this = this;
            this.formCell({
                apply: function (value) {
                    _this.cell_id = value;
                    _this.set_place();
                },
                cancel: function () {
                    _this.scan_pallet();
                }
            });
        };

        Allocation.prototype.set_place = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/alloc/set_place",
                data: {
                    cell_id: this.cell_id,
                    pallet_id: this.pallet_id },
                success: function () {
                    _this.complete("Паллета была успешно размещена");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return Allocation;
    })(TaskModule.Task);
    AllocationModule.Allocation = Allocation;
})(AllocationModule || (AllocationModule = {}));
var MovingModule;
(function (MovingModule) {
    var Moving = (function (_super) {
        __extends(Moving, _super);
        function Moving() {
            _super.apply(this, arguments);
            this.class_name = "Moving";
        }
        Moving.prototype.start = function () {
            _super.prototype.start.call(this);

            this.getCellDestination();
        };

        Moving.prototype.getCellDestination = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/task/getcelldestination",
                data: { 'task_id': this.task_id },
                success: function (resp) {
                    _this.cell_name = resp["cell_name"];
                    _this.cell_id = resp["cell_id"];

                    if (resp["target_id"]) {
                        _this.target_id = resp.target_id;
                        _this.target_name = resp.target_name;
                    }

                    _this.scanCell();
                },
                error: function () {
                    _this.stop();
                }
            });
        };

        Moving.prototype.scanCell = function () {
            var _this = this;
            this.formCell({
                text: "Перемещение с адреса: " + this.cell_name,
                expected: this.cell_id,
                apply: function (value) {
                    _this.cell_id = value;
                    _this.palletConfirm();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        Moving.prototype.palletConfirm = function () {
            var _this = this;
            var form = new FormModule.Form();

            form.FormMenu({
                caption: "Подтверждение погрузки паллеты",
                buttons: {
                    "Паллета погружена": function () {
                        _this.scanParty();
                    },
                    "Ячейка была пуста": function () {
                        //SendFail(curr_CellBarcode, 0, 0, 0, ERR_EMPTYCELL);
                        _this.stop();
                    }
                }
            });
        };

        Moving.prototype.scanParty = function () {
            var _this = this;
            this.formParty({
                apply: function (value) {
                    _this.party_id = value;
                    _this.checkParty();
                },
                cancel: function () {
                    _this.palletConfirm();
                }
            });
        };

        Moving.prototype.checkParty = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/valid",
                data: {
                    'cell_id': this.cell_id,
                    'party_id': this.party_id
                },
                success: function (resp) {
                    _this.scanTarget();
                },
                error: function () {
                    _this.scanParty();
                }
            });
        };

        Moving.prototype.scanTarget = function () {
            var _this = this;
            if (!this.target_id) {
                this.palletMove();

                //this.complete("Отвезите паллету в зону отгрузки");
                return;
            }

            this.formCell({
                text: "Перемещение на адрес: " + this.target_name,
                expected: this.target_id,
                apply: function (value) {
                    _this.target_id = value;
                    _this.targetConfirm();
                },
                cancel: function () {
                    _this.scanParty();
                }
            });
        };

        Moving.prototype.targetConfirm = function () {
            var _this = this;
            this.menu({
                caption: "Подтверждение погрузки паллеты",
                buttons: {
                    "Паллета размещена": function () {
                        _this.palletMove();
                    },
                    "Ячейка была занята": function () {
                        _this.nextCell(); // получим новый адрес
                    }
                }
            });
        };

        Moving.prototype.nextCell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/moving/next_cell",
                data: {
                    'cell_id': this.cell_id,
                    'party_id': this.party_id,
                    'target_id': this.target_id
                },
                success: function (resp) {
                    _this.target_id = resp.target_id;
                    _this.target_name = resp.target_name;

                    _this.scanTarget();
                },
                error: function () {
                    _this.stop();
                }
            });
        };

        Moving.prototype.palletMove = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/moving/moved",
                data: {
                    'cell_id': this.cell_id,
                    'target_id': this.target_id
                },
                success: function (resp) {
                    _this.complete("Паллета была успешно размещена");
                },
                error: function () {
                    _this.stop();
                }
            });
        };
        return Moving;
    })(TaskModule.Task);
    MovingModule.Moving = Moving;
})(MovingModule || (MovingModule = {}));
var OrderBatchingModule;
(function (OrderBatchingModule) {
    var OrderBatching = (function (_super) {
        __extends(OrderBatching, _super);
        function OrderBatching() {
            _super.apply(this, arguments);
            this.class_name = "OrderBatching";
        }
        OrderBatching.prototype.start = function () {
            _super.prototype.start.call(this);

            this.getPallet();
        };

        /**
        *	сканирование ШК паллеты для сборки
        */
        OrderBatching.prototype.getPallet = function () {
            var _this = this;
            this.formPallet({
                apply: function (value) {
                    _this.pallet_id = value;
                    _this.bind_pallet();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        OrderBatching.prototype.bind_pallet = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/batching/bind_pallet",
                data: {
                    task_id: this.task_id,
                    pallet_id: this.pallet_id
                },
                success: function () {
                    _this.printMarks();
                },
                error: function () {
                    _this.getPallet();
                }
            });
        };

        //-----------------------------------------------------------------------------
        //Отправить к бригадиру
        //-----------------------------------------------------------------------------
        OrderBatching.prototype.printMarks = function () {
            var _this = this;
            this.menu({
                caption: "Печать этикеток",
                text: "Пожалуйста, распечатайте партионные наклейки в Шиве, затем нажмите кнопку 'Приступить к сборке'",
                buttons: {
                    "Приступить к сборке": function () {
                        _this.get_cell();
                    },
                    "Отмена": function () {
                        _this.stop();
                    }
                }
            });
        };

        /**
        *  вызов shiva.getCellValFromPackList()
        */
        OrderBatching.prototype.get_cell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/batching/get_cell",
                data: {
                    header_id: this.header_id,
                    pallet_id: this.pallet_id
                },
                success: function (resp) {
                    _this.value = resp.value; // Сколько нужно взять
                    _this.count = resp.count; // Сколько уже собрано
                    _this.count_total = resp.count_total; // Сколько всего нужно собрать
                    _this.product_name = resp.product_name;
                    _this.packlist_id = resp.packlist_id;

                    if (resp["cell_id"]) {
                        _this.cell_id = resp.cell_id;
                        _this.cell_name = resp.cell_name;

                        _this.scan_cell();
                    } else if (resp["target_id"]) {
                        _this.target_id = resp.target_id;
                        _this.target_name = resp.target_name;

                        _this.scan_target();
                    } else {
                        _this.complete("Пожалуйста, отвезите паллету в зону сборки и нажмите кнопку [завершить задачу]");
                    }
                },
                error: function () {
                    _this.printMarks();
                }
            });
        };

        /**
        *   Ввод ШК ячейки с товаром из которой будет браться товар
        */
        OrderBatching.prototype.scan_cell = function () {
            var _this = this;
            var msg = "Взять коробок: <b>" + this.value + "</b></br>C адреса: " + this.cell_name + "</br>" + this.product_name;

            this.formCell({
                caption: "собрано " + this.count + " позиций из " + this.count_total,
                text: msg,
                expected: this.cell_id,
                apply: function (value) {
                    _this.cell_id = value;

                    _this.getCount();
                },
                cancel: function () {
                    _this.stop();
                }
            });
        };

        /**
        *   Target Cell
        *   Ввод ШК ячейки с товаром из которой будет браться товар
        */
        OrderBatching.prototype.scan_target = function () {
            var _this = this;
            this.formBarcode({
                caption: "Ввод штрих-кода целевой ячейки",
                text: "Поместить на адрес: " + this.target_name,
                expected: this.target_id,
                apply: function (value) {
                    _this.target_id = value;
                    _this.setPalletToDelivery();
                },
                cancel: function () {
                    _this.get_cell();
                }
            });
        };

        /**
        *   Ввод количества погруженных коробок
        *
        */
        OrderBatching.prototype.getCount = function () {
            var _this = this;
            var msg = "Необходимо погрузить " + this.value + " коробок.</br>Введите число погруженных коробок";

            this.formCount({
                text: msg,
                apply: function (value) {
                    _this.getConfirm(value);
                },
                cancel: function () {
                    _this.scan_cell();
                }
            });
        };

        /**
        *   Подтверждение количества погруженных коробок
        *
        */
        OrderBatching.prototype.getConfirm = function (value) {
            var _this = this;
            this.menu({
                caption: "Подтверждение",
                text: "С адреса: " + this.cell_name + "</br>взято коробок:" + value,
                buttons: {
                    "Продолжить": function () {
                        _this.value = value;
                        _this.ok_cell();
                    },
                    "Вернуться": function () {
                        _this.getCount();
                    }
                }
            });
        };

        OrderBatching.prototype.ok_cell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/batching/ok_cell",
                data: {
                    pallet_id: this.pallet_id,
                    cell_id: this.cell_id,
                    count: this.value,
                    party_id: this.party_id,
                    extra_party_id: this.extra_party_id,
                    packlist_id: this.packlist_id
                },
                success: function () {
                    _this.add_again();
                },
                error: function () {
                    _this.get_cell();
                }
            });
        };

        /*
        * Вернуться и взять ещё
        */
        OrderBatching.prototype.add_again = function () {
            this.get_cell();
        };

        OrderBatching.prototype.setPalletToDelivery = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/batching/set_pallet",
                data: {
                    pallet_id: this.pallet_id,
                    target_id: this.target_id
                },
                success: function (resp) {
                    _this.complete("Задание окончено, нажмите кнопку [завершить задачу]");
                },
                error: function () {
                    _this.get_cell();
                }
            });
        };
        return OrderBatching;
    })(TaskModule.Task);
    OrderBatchingModule.OrderBatching = OrderBatching;
})(OrderBatchingModule || (OrderBatchingModule = {}));
/// <reference path="orderbatching.ts" />
var OrderBatchingRawModule;
(function (OrderBatchingRawModule) {
    var OrderBatchingRaw = (function (_super) {
        __extends(OrderBatchingRaw, _super);
        function OrderBatchingRaw() {
            _super.apply(this, arguments);
            this.class_name = "OrderBatchingRaw";
        }
        /**
        *   Ввод ШК ячейки с товаром из которой будет браться товар
        */
        OrderBatchingRaw.prototype.scan_cell = function () {
            var _this = this;
            this.party_id = "";

            var msg = "Взять коробок: <b>" + this.value + "</b></br>C адреса: " + this.cell_name + "</br>" + this.product_name;

            this.formCell({
                caption: "собрано " + this.count + " позиций из " + this.count_total,
                text: msg,
                expected: this.cell_id,
                apply: function (value) {
                    _this.cell_id = value;

                    _this.getCount();
                },
                cancel: function () {
                    _this.get_cell();
                }
            });
        };

        /**
        *   Ввод количества погруженных коробок
        *
        */
        OrderBatchingRaw.prototype.getCount = function () {
            var _this = this;
            var msg = "Необходимо погрузить сырья в количесте <b>" + this.value + "</b></br>Введите количество погруженного сырья";

            this.formCount({
                text: msg,
                apply: function (value) {
                    _this.getConfirm(value);
                },
                cancel: function () {
                    _this.scan_cell();
                }
            });
        };

        /**
        *   Подтверждение количества погруженных коробок
        *
        */
        OrderBatchingRaw.prototype.getConfirm = function (value) {
            var _this = this;
            this.menu({
                caption: "Подтверждение",
                text: "С адреса: " + this.cell_name + "</br>взято сырья:" + value,
                buttons: {
                    "Продолжить": function () {
                        _this.value = value;

                        if (_this.party_id != "") {
                            _this.scan_extra_party();
                        } else {
                            _this.scan_party(); ///  отличие от обычной сборки
                        }
                    },
                    "Вернуться": function () {
                        _this.getCount();
                    }
                }
            });
        };

        OrderBatchingRaw.prototype.scan_party = function () {
            var _this = this;
            this.formParty({
                text: "Введите штрих-код <b>ПАРТИИ</b> сырья",
                apply: function (value) {
                    _this.party_id = value;

                    _this.scan_extra_party();
                },
                cancel: function () {
                    /*this.getConfirm();*/
                    _this.stop();
                }
            });
        };

        OrderBatchingRaw.prototype.scan_extra_party = function () {
            var _this = this;
            this.formParty({
                text: "Введите штрих-код <b>ПОДПАРТИИ</b> сырья",
                apply: function (value) {
                    _this.extra_party_id = value;

                    _this.ok_cell();
                },
                cancel: function () {
                    _this.scan_party();
                }
            });
        };

        OrderBatchingRaw.prototype.add_again = function () {
            var _this = this;
            this.menu({
                caption: "Подтверждение",
                /*text:    "Вы можете продолжить сборку сырья, либо взять ещё такое же сырье из этой же ячейки",*/
                buttons: {
                    "Cледующая позиция": function () {
                        /* Получить новую ячейку для сборки*/
                        _this.get_cell();
                    },
                    "Взять такое же кол-во": function () {
                        /* Чтобы взять такую же коробку с таким же количеством сырья
                        * и заново не сканировать партии
                        * то перебрасываем сразу на сканировании подпартии
                        */
                        _this.scan_extra_party();
                    },
                    "Взять другое кол-во": function () {
                        /* В случае если мы хотим взять из той же ячейки коробку с другим количеством,
                        * то заново просим ввести количество*/
                        _this.getCount();
                    },
                    "Заблокировать ячейку": function () {
                        /* Заблокировать ячейку и сообщить об ошибке. Получить новую ячейку для сборки*/
                        _this.block_cell();
                    },
                    "Закончить эту паллету": function () {
                        /* Если на паллете закончилось место, то берем новую паллету */
                        _this.end_pallet_raw();
                    }
                }
            });
        };

        OrderBatchingRaw.prototype.block_cell = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/batching/ok_cell",
                data: {
                    pallet_id: this.pallet_id,
                    cell_id: this.cell_id,
                    count: "0",
                    party_id: this.party_id,
                    extra_party_id: this.extra_party_id,
                    packlist_id: this.packlist_id
                },
                success: function () {
                    _this.get_cell();
                },
                error: function () {
                    _this.get_cell();
                }
            });
        };

        OrderBatchingRaw.prototype.end_pallet_raw = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/batching/end_pallet_raw",
                data: {
                    pallet_id: this.pallet_id
                },
                success: function (resp) {
                    _this.target_id = resp.target_id;
                    _this.target_name = resp.target_name;

                    _this.scan_target_raw();
                },
                error: function () {
                    _this.add_again();
                }
            });
        };

        OrderBatchingRaw.prototype.scan_target_raw = function () {
            var _this = this;
            this.formBarcode({
                caption: "Ввод штрих-кода целевой ячейки",
                text: "Поместить на адрес: " + this.target_name,
                expected: this.target_id,
                apply: function (value) {
                    _this.target_id = value;
                    _this.setPalletToDelivery_raw();
                },
                cancel: function () {
                    _this.add_again();
                }
            });
        };

        OrderBatchingRaw.prototype.setPalletToDelivery_raw = function () {
            var _this = this;
            this.ajax({
                type: "POST",
                url: "/mbl/batching/set_pallet",
                data: {
                    pallet_id: this.pallet_id,
                    target_id: this.target_id
                },
                success: function (resp) {
                    _this.getPallet();
                },
                error: function () {
                    _this.get_cell();
                }
            });
        };
        return OrderBatchingRaw;
    })(OrderBatchingModule.OrderBatching);
    OrderBatchingRawModule.OrderBatchingRaw = OrderBatchingRaw;
})(OrderBatchingRawModule || (OrderBatchingRawModule = {}));
//# sourceMappingURL=release.js.map
