/*************************************************************************************************
* name - название cookie.                                                                        *
* value - значение cookie.                                                                       *
* props - объект с дополнительными свойствами для установки cookie:                              *
*     expires - Время истечения cookie. Интерпретируется по-разному, в зависимости от типа:      *
*               Если число - количество секунд до истечения.                                     *
*               Если объект типа Date - точная дата истечения.                                   *
*               Если expires в прошлом, то cookie будет удалено.                                 *
*               Если expires отсутствует или равно 0, то cookie будет установлено как сессионное *
*               и исчезнет при закрытии браузера.                                                *
*     domain - домен, для которого значение cookie действительно. Например, "javascript.ru".     *
*              В этом случае cookie будет действительно и для домена javascript.ru, и для        *
*              www.javascript.ru. Если атрибут опущен, то используется доменное имя сервера, на  *
*              котором было задано значение cookie.                                              *
*     path - устанавливает подмножество документов, для которых действительно значение cookie.   *
*            Для того, чтобы cookie отсылались при каждом запросе к серверу, необходимо указать  *
*            корневой каталог сервера, например, "path=/". Если атрибут не указан, то значение   *
*            cookie распространяется только на документы в той же директории, что и документ, в  *
*            котором было установлено значение cookie.                                           *
*     secure - пересылать cookie только через HTTPS.                                             *
* Примеры:                                                                                       *
*  setCookie("name", "123", { expires: 120} ) // поставить куку на 120 секунд                    *
*************************************************************************************************/
function setCookie(name, value, props) {
	props = props || {}
	var exp = props.expires
	if (typeof exp == "number" && exp) {
		var d = new Date()
		d.setTime(d.getTime() + exp*1000)
		exp = props.expires = d
	}
	if(exp && exp.toUTCString) { props.expires = exp.toUTCString() }

	value = encodeURIComponent(''+value);
	var updatedCookie = name + "=" + value
	for(var propName in props){
		updatedCookie += "; " + propName
		var propValue = props[propName]
		if(propValue !== true){ updatedCookie += "=" + propValue }
	}
	document.cookie = updatedCookie

}

/*************************************************************************************************
*  возвращает cookie если есть или undefined                                                     *
*************************************************************************************************/
function getCookie(name) {
	var matches = document.cookie.match(new RegExp(
	  "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
	))
	return matches ? decodeURIComponent(matches[1]) : undefined 
}

/*************************************************************************************************
* удаляет cookie                                                                                 *
*************************************************************************************************/
function deleteCookie(name, path, domain) {
	setCookie(name, null, { expires: -1 })
}
