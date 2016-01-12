var HzwCityPicker = function(a) {
		this.template = $('<div class="hzw-city-picker" id="hzw_city_picker"><div class="hzw-hot-wrap"><p>热门城市</p><ul id="hzw_hot_city"></ul></div><div class="line"></div><div class="hzw-wrap"><p>选择省份</p><ul class="hzw-province-wrap" id="hzw_province_wrap"></ul></div></div>');
		this.hot_city = $('#hzw_hot_city', this.template);
		this.province_wrap = $('#hzw_province_wrap', this.template);
		this.settings = {
			data: a.data,
			target: $('#' + a.target),
			valType: a.valType || 'k',
			multiple: a.multiple || false
		};
		this.hideProvinceInput = a.hideProvinceInput ? $('<input>', {
			type: 'hidden',
			name: a.hideProvinceInput.name,
			id: a.hideProvinceInput.id,
			val: a.hideProvinceInput.val || ''
		}) : false;
		this.hideCityInput = $('<input>', {
			type: 'hidden',
			name: a.hideCityInput.name,
			id: a.hideCityInput.id,
			val: a.hideCityInput.val || ''
		});
		this.callback = a.callback || '';
		this.flag = true
	};
HzwCityPicker.prototype = {
	init: function() {
		var a = this;
		if($('#'+a.hideCityInput.attr('id')).size()==0){
			a.settings.target.after(a.hideCityInput);
		}else{
			a.hideCityInput = $('#'+a.hideCityInput.attr('id'));
		}
		if (a.hideProvinceInput) {
			if($('#'+a.hideProvinceInput.attr('id')).size()==0){
				a.settings.target.after(a.hideProvinceInput);
			}else{
				a.hideProvinceInput = $('#'+a.hideProvinceInput.attr('id'));
			}
		}
		a.addTargetEvent()
	},
	buildCityPicker: function() {
		var a = this;
		a.addHotCityTpl();
		a.addProvinceTpl();
		a.addMouseEvent();
		a.addProvinceEvent();
		a.addCityEvent()
	},
	addHotCityTpl: function() {
		var a = this;
		var b = a.settings.data.hot;
		var c = '';
		for (var i = 0, len = b.length; i < len; i++) {
			c += '<li class="hzw-hot-city" data-id="' + b[i]['id'] + '" data-name="' + b[i]['name'] + '" data-pid="' + b[i]['pid'] + '" data-pname="' + b[i]['pname'] + '">' + b[i]['name'] + '</li>'
		}
		a.hot_city.html(c)
	},
	addProvinceTpl: function() {
		var a = this;
		var b = a.settings.data.province;
		var c = '';
		for (var i = 0, len = b.length; i < len; i++) {
			c += '<li class="hzw-province" data-id="' + b[i]['id'] + '" data-name="' + b[i]['name'] + '"><ul class="hzw-city-wrap"></ul><div class="hzw-province-name">' + b[i]['name'] + '</div></li>'
		}
		a.province_wrap.html(c)
	},
	addCityTpl: function(a) {
		var b = this;
		var c = a.data('id');
		var d = a.position();
		var e = b.settings.data.province;
		var f;
		var g = '';
		for (var i = 0, plen = e.length; i < plen; i++) {
			if (e[i]['id'] == parseInt(c)) {
				f = e[i]['city'];
				break
			}
		}
		for (var j = 0, clen = f.length; j < clen; j++) {
			g += '<li class="hzw-city" data-id="' + f[j]['id'] + '" data-name="' + f[j]['name'] + '" title="' + f[j]['name'] + '">' + f[j]['name'] + '</li>'
		}
		var node = a.find('.hzw-city-wrap');
		node.html(g);
		node.show();
		if((d.top + node.height()) > 410 ) {
			node.css({left:'-' + (d.left - 53) + 'px',top:'-' + (node.height()+21)+'px'});
		}else{
			node.css({left:'-' + (d.left - 53) + 'px'});
		}
	},
	addMouseEvent: function() {
		var a = this;
		a.template.mouseenter(function() {
			a.flag = false
		}).mouseleave(function() {
			a.flag = true
		})
	},
	addProvinceEvent: function() {
		var b = this;
		b.province_wrap.on('click', '.hzw-province', function() {
			var a = $(this);
			if (!a.hasClass('active')) {
				b.province_wrap.find('.hzw-province').removeClass('active');
				b.province_wrap.find('.hzw-province-name').removeClass('active');
				b.province_wrap.find('.hzw-city-wrap').hide().children().remove();
				a.addClass('active');
				a.find('.hzw-province-name').addClass('active');
				b.addCityTpl(a)
			} else {
				a.removeClass('active');
				a.find('.hzw-province-name').removeClass('active');
				a.find('.hzw-city-wrap').hide().children().remove()
			}
		})
	},
	addCityEvent: function() {
		var g = this;
		g.hot_city.on('click', '.hzw-hot-city', function() {
			var a = $(this);
			var b = a.data('id');
			var c = a.data('name');
			g.settings.target.val(c);
			if (g.settings.valType == 'k-v') {
				g.hideCityInput.val(b + '-' + c)
			} else if (g.settings.valType == 'v') {
				g.hideCityInput.val(c)
			} else {
				g.hideCityInput.val(b)
			}
			if (g.hideProvinceInput) {
				var d = a.data('pid');
				var e = a.data('pname');
				if (g.settings.valType == 'k-v') {
					g.hideProvinceInput.val(d + '-' + e)
				} else if (g.settings.valType == 'v') {
					g.hideProvinceInput.val(e)
				} else {
					g.hideProvinceInput.val(d)
				}
			}
			g.template.remove();
			if (g.callback) g.callback()
		});
		g.province_wrap.on('click', '.hzw-city', function() {
			var a = $(this);
			var b = a.data('id');
			var c = a.data('name');
			g.settings.target.val(c);
			if (g.settings.valType == 'k-v') {
				g.hideCityInput.val(b + '-' + c)
			} else if (g.settings.valType == 'v') {
				g.hideCityInput.val(c)
			} else {
				g.hideCityInput.val(b)
			}
			if (g.hideProvinceInput) {
				var d = a.parent().parent();
				var e = d.data('id');
				var f = d.data('name');
				if (g.settings.valType == 'k-v') {
					g.hideProvinceInput.val(e + '-' + f)
				} else if (g.settings.valType == 'v') {
					g.hideProvinceInput.val(f)
				} else {
					g.hideProvinceInput.val(e)
				}
			}
			g.template.remove();
			if (g.callback) g.callback()
		})
	},
	addTargetEvent: function() {
		var d = this;
		d.settings.target.focus(function() {
			var a = $(this);
			d.buildCityPicker();
			var b = a.offset();
			var c = b.top + a.outerHeight() + 15;
			if(c+650 > $(window).height()){
				c =  $(window).height() - 650;
			}
			d.template.css({
				'left': b.left,
				'top': c
			});
			$('body').append(d.template)
		}).blur(function() {
			if (d.flag) {
				d.template.remove();
				d.flag = true
			}
		})
	}
};