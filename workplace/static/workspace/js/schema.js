// workplace/static/workspace/js/schema.js
$(document).ready(() => {
	axios.defaults.withCredentials = true;
	axios.defaults.xsrfCookieName = 'csrftoken';
	axios.defaults.xsrfHeaderName = 'X-CSRFToken';
	
	const interval = 15;
	
	const handleChangeNumsRow = (e) => {
		const nums = $(e.target);
		if (+nums.attr('min') <= +nums.val() && +nums.val() <= +nums.attr('max')) {
			$('#btnGenerateData').attr('disabled', false);
		} else {
			$('#btnGenerateData').attr('disabled', true);
		}
	};
	const appendTableRow = (task_id) => {
		const tb = $('tbody');
		const tr = tb.children().last();
		const trc = $($('script[data-template="appendTableRow"]').html().trim()).clone();
		const nums_row = tr.find('#index').text();
		trc.attr('task_id', task_id);
		trc.children('#index').text((nums_row ? +nums_row : 0) + 1);
		trc.find('#date_created').text((new Date()).toISOString().split('T') [0]);
		trc.find('#status').text('Processing');
		tb.append(trc);
	};
	const handleSuccessCreateDataSet = (tasks, urls) => {
		tasks.forEach((task_id) => {
			const tr = $('tr[task_id=' + task_id + ']');
			const elem_status = tr.find('#status');
			elem_status.removeClass('badge-secondary');
			elem_status.addClass('badge-success');
			elem_status.text('Ready');
			const elem_download = tr.find('#download');
			elem_download.removeClass('d-none');
			elem_download.attr('href', urls[task_id]);
			tr.removeAttr('task_id');
		})
	};
	const handleErrorCreateDataSet = () => {
		const tb = $('tbody');
		tb.children().last().remove();
	};
	const getTaskStatus = () => {
		let task_id_list = [];
		const tb = $('tbody');
		const url = tb.attr('link-check-status');
		const trs = tb.children('tr');
		trs.each((i, el) => {
			if (el.hasAttribute('task_id')) {
				task_id_list.push($(el).attr('task_id'));
			}
		});
		if (task_id_list.length > 0) {
			axios
				.post(url, {task_id_list: task_id_list})
				.then(r => {
					handleSuccessCreateDataSet(r.data.tasks, r.data.urls)
				})
				.catch(error => {
					console.log(error.data.message)
				});
		}
	};
	
	setInterval(getTaskStatus, interval * 1000);
	
	$('#numsRow').keyup(handleChangeNumsRow);
	$('#btnGenerateData').click((e) => {
		const nums = $('#numsRow');
		const btnGenerateData = $(e.target);
		const form = $('#formGenerateData');
		btnGenerateData.prop('disabled', true);
		axios.get(form[0].action, {
			params: {
				nums_row: nums.val(),
			}
		}).then(respone => {
			appendTableRow(respone.data.task_id);
		}).catch(error => {
			handleErrorCreateDataSet();
		}).then(() => btnGenerateData.prop('disabled', false));
	});
});
