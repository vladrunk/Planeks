// workplace/static/workspace/js/schema.js
$(document).ready(() => {
	axios.defaults.withCredentials = true;
	axios.defaults.xsrfCookieName = 'csrftoken';
	axios.defaults.xsrfHeaderName = 'X-CSRFToken';
	
	const interval = 10;
	
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
	const handleSuccessCreateDataSet = (tasks, datasets) => {
		tasks.forEach((task_id) => {
			const tr = $('tr[task_id=' + task_id + ']');
			
			const elem_status = tr.find('#status');
			elem_status.removeClass('badge-secondary');
			elem_status.addClass('badge-success');
			elem_status.text('Ready');
			
			const elem_download = tr.find('#btnDownload');
			elem_download.removeClass('d-none');
			elem_download.click(handleClickBtnDownload);
			
			const elem_ds_id = tr.find('#datasetId');
			elem_ds_id.text(datasets[task_id]);
			
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
	const handleClickBtnDownload = (e) => {
		const btn = e.target;
		const a = btn.previousElementSibling;
		const dataset_id = a.innerText;
		const url = a.href;
		axios
			.get(url, {
				params: {
					dataset_id: dataset_id,
				}
			})
			.then(response => {
				handleSuccessDownload(response.data.content_b64)
			})
			.catch(error => {
				console.log(error.data.message)
			})
		
	};
	const b64toBlob = (b64Data, contentType = '', sliceSize = 512) => {
		const byteCharacters = atob(b64Data);
		const byteArrays = [];
		
		for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
			const slice = byteCharacters.slice(offset, offset + sliceSize);
			
			const byteNumbers = new Array(slice.length);
			for (let i = 0; i < slice.length; i++) {
				byteNumbers[i] = slice.charCodeAt(i);
			}
			
			const byteArray = new Uint8Array(byteNumbers);
			byteArrays.push(byteArray);
		}
		
		return new Blob(byteArrays, {type: contentType});
	}
	const handleSuccessDownload = (b64Data) => {
		const contentType = 'text/csv';
		const blob = b64toBlob(b64Data, contentType);
		const blobUrl = URL.createObjectURL(blob);
		let link = document.createElement('a');
		link.download = 'dataset.csv';
		link.href = blobUrl;
		link.click();
		URL.revokeObjectURL(link.href);
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
	$('button#btnDownload').each((i, el) => {
		$(el).click(handleClickBtnDownload);
	});
});
