// workplace/static/workspace/js/index.js
$(document).ready(() => {
	// Удаляем строку с таблицы
	const DeleteRowFromTable = (e) => {
		$(e).closest('tr').remove();
	};
	// Изменяем состояние кнопки
	const toggleAllBtnState = (e, enable) => {
		const func = enable ? setBtnEnable : setBtnDisable;
		$(e).closest('tr').find('div').each((i, el) => {
			const src = $(el).children('a').first();
			const tmp = $(el).children('a').last();
			const btn = $(el).find('input').first();
			func(src, tmp, btn);
		})
	}
	// Вкл кнопку
	const setBtnEnable = (src, tmp, btn) => {
		console.log('setBtnEnable', btn);
		src.click(handleClickBtnDelete);
		setBtnState(src, tmp, btn, false);
	}
	// Выкл кнопку
	const setBtnDisable = (src, tmp, btn) => {
		console.log('setBtnDisable', btn);
		src.unbind();
		setBtnState(tmp, src, btn, true);
	}
	// Установка состояния
	const setBtnState = (a, b, c, state) => {
		a.attr('href', b.attr('href'));
		b.removeAttr('href');
		c.attr('disabled', state);
	}
	// Обаботчик клика по кнопке
	const handleClickBtnDelete = e => {
		e.preventDefault();
		const url = e.target.parentNode.href;
		toggleAllBtnState(e.target, false);
		axios
			.get(url)
			.then(() => DeleteRowFromTable(e.target))
			.catch(() => toggleAllBtnState(e.target, true));
	};
	// Присваиваем каждой кнопке обработчик
	$('a#btnDeleteSchema').each((i, el) => {
		$(el).click(handleClickBtnDelete);
	})
});