// workplace/static/workspace/js/script.js
$(document).ready(() => {
	
	const handleClickDelete = (e) => {
		$(e.target).closest('#columnRow').remove();
	};
	
	const handleClickClear = (e) => {
		const cols = $(e.target).closest('#columnRow');
		$(cols).find('input, select').each((i, el) => {
			el.value = '';
			if (el.name === 'from' || el.name === 'to') {
				const parent = $(el.parentNode)
				if (!parent.hasClass('invisible')) {
					parent.addClass('invisible');
				}
			}
		});
	};
	
	const handleChangeType = (e) => {
		let inputsFromTo = [
			$(e.target).closest('div.form-group').next(),
			$(e.target).closest('div.form-group').next().next()
		];
		
		if ($(e.target).val() === "integer") {
			inputsFromTo.forEach((el) => {
				el.removeClass('invisible');
			})
		} else {
			inputsFromTo.forEach((el) => {
				el.children('input').first().val(0);
				el.addClass('invisible');
			})
		}
	};
	
	const calcOrder = (cols_exst) => {
		
		let max_order = -1;
		
		cols_exst.children().each((i, el) => {
			const el_order = $(el).find('#inputColumnOrder').val();
			max_order = +max_order > +el_order
				? +max_order
				: +el_order;
		})
		
		return max_order + 1;
	}
	
	$('button#btnDeleteColumn').each((i, el) => {
		$(el).click(handleClickDelete);
	});
	
	$('button#btnClearColumn').click(handleClickClear);
	
	$('select#inputColumnType').each((i, el) => {
		$(el).change(handleChangeType);
	});
	
	$("#formApend").submit(e => {
		e.preventDefault();
		
		let cols_exst = $('#formSend'); // Существующие строки
		let col_added = $('#formApend #columnRow'); // Строка, что добавляем
		let temp = $($('script[data-template="appendColumn"]').html().trim()).clone(); // Шаблон
		
		let name = temp.find('#inputColumnName')[0]
		name.value = col_added.find("#inputColumnName")[0].value;
		
		let type = temp.find('#inputColumnType')[0]
		type.value = col_added.find("#inputColumnType")[0].value;
		type.onchange = handleChangeType;
		
		let from = temp.find('#inputColumnRangeFrom')[0]
		from.value = col_added.find("#inputColumnRangeFrom")[0].value;
		$(from).closest('div').attr('class',
			$(col_added.find("#inputColumnRangeFrom")[0]).closest('div').attr('class')
		);
		
		let to = temp.find('#inputColumnRangeTo')[0]
		to.value = col_added.find("#inputColumnRangeTo")[0].value;
		$(to).closest('div').attr('class',
			$(col_added.find("#inputColumnRangeTo")[0]).closest('div').attr('class')
		);
		
		let order = temp.find('#inputColumnOrder')[0]
		order.value = col_added.find("#inputColumnOrder")[0].value
			? col_added.find("#inputColumnOrder")[0].value
			: calcOrder(cols_exst);
		
		let btn = temp.find('#btnDeleteColumn')[0]
		btn.onclick = handleClickDelete;
		
		temp.appendTo(cols_exst);
		$('button#btnClearColumn').click();
	});
});