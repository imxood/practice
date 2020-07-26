## ubuntu环境

    pip3 install --user scons
    sudo apt-get install libsndio-dev libgtk-3-dev libglu1-mesa libglu1-mesa-dev libgl1-mesa-glx libgl1-mesa-dev libasound2-dev git vim clang-format

## 缺少hb.h

3rd/SDL/SConscript:60

添加:
    '/usr/include/harfbuzz'

## 开发

	fontgen 位图字体生成工具
	imagegen 位图图片生成工具
	resgen 二进制文件生成资源常量数组
	themegen XML 主题转换成二进制的主题
	xml_to_ui XML 的界面描述格式转换二进制的界面描述格式
	update_res.py 批量转换整个项目的资源


## 移植awtk 到 stm32 rt-thread中

	1. 首先确定屏幕的坐标系

		   竖屏时， 以左上角位原点， x向右为正， y向下为正，
		   横屏时， 同上

	2， 编译

		CDEFINE:
			'HAS_AWTK_CONFIG', 'ARM_MATH_CM7'

		INCLUDES:
			"src",
			"src/ext_widgets",
			"3rd",
			"3rd/agge",
			"3rd/libunibreak",
			"3rd/stb",
			"3rd/nanovg",
			"3rd/nanovg/base",
			"3rd/SDL/include",

		SOURCES:
			'3rd/agge/agge/math.cpp',
			'3rd/agge/agge/stroke.cpp',
			'3rd/agge/agge/stroke_features.cpp',
			'3rd/agge/agge/vector_rasterizer.cpp',
			'3rd/libunibreak/emojidef.c',
			'3rd/libunibreak/graphemebreak.c',
			'3rd/libunibreak/linebreak.c',
			'3rd/libunibreak/linebreakdata.c',
			'3rd/libunibreak/linebreakdef.c',
			'3rd/libunibreak/unibreakbase.c',
			'3rd/libunibreak/unibreakdef.c',
			'3rd/libunibreak/wordbreak.c',
			'3rd/nanovg/agge/nanovg_agge.cpp',
			'3rd/nanovg/agge/nanovg_vertex.cpp',
			'3rd/nanovg/base/nanovg.c',
			'src/awtk_global.c',
			'src/base/asset_loader.c',
			'src/base/asset_loader_default.c',
			'src/base/assets_manager.c',
			'src/base/bitmap.c',
			'src/base/canvas.c',
			'src/base/children_layouter.c',
			'src/base/children_layouter_factory.c',
			'src/base/clip_board.c',
			'src/base/date_time_format.c',
			'src/base/dialog.c',
			'src/base/dialog_highlighter.c',
			'src/base/dialog_highlighter_factory.c',
			'src/base/data_reader_asset.c',
			'src/base/enums.c',
			'src/base/event_queue.c',
			'src/base/events.c',
			'src/base/font.c',
			'src/base/font_loader.c',
			'src/base/font_manager.c',
			'src/base/glyph_cache.c',
			'src/base/graphic_buffer.c',
			'src/base/hscrollable.c',
			'src/base/idle.c',
			'src/base/image_base.c',
			'src/base/image_loader.c',
			'src/base/image_manager.c',
			'src/base/layout.c',
			'src/base/lcd.c',
			'src/base/lcd_profile.c',
			'src/base/line_break.c',
			'src/base/locale_info.c',
			'src/base/main_loop.c',
			'src/base/native_window.c',
			'src/base/self_layouter.c',
			'src/base/self_layouter_factory.c',
			'src/base/shortcut.c',
			'src/base/style.c',
			'src/base/style_const.c',
			'src/base/style_factory.c',
			'src/base/style_mutable.c',
			'src/base/suggest_words.c',
			'src/base/system_info.c',
			'src/base/text_edit.c',
			'src/base/theme.c',
			'src/base/timer.c',
			'src/base/ui_builder.c',
			'src/base/ui_feedback.c',
			'src/base/ui_loader.c',
			'src/base/velocity.c',
			'src/base/vgcanvas.c',
			'src/base/widget.c',
			'src/base/widget_animator.c',
			'src/base/widget_animator_factory_null.c',
			'src/base/widget_animator_manager.c',
			'src/base/widget_factory.c',
			'src/base/widget_vtable.c',
			'src/base/window.c',
			'src/base/window_animator.c',
			'src/base/window_animator_factory.c',
			'src/base/window_base.c',
			'src/base/window_manager.c',
			'src/blend/blend_image_bgr565_bgr565.c',
			'src/blend/blend_image_bgr565_bgra8888.c',
			'src/blend/blend_image_bgr565_rgb565.c',
			'src/blend/blend_image_bgr565_rgba8888.c',
			'src/blend/blend_image_bgr888_bgr565.c',
			'src/blend/blend_image_bgr888_bgr888.c',
			'src/blend/blend_image_bgr888_bgra8888.c',
			'src/blend/blend_image_bgr888_rgb565.c',
			'src/blend/blend_image_bgr888_rgba8888.c',
			'src/blend/blend_image_bgra8888_bgr565.c',
			'src/blend/blend_image_bgra8888_bgra8888.c',
			'src/blend/blend_image_bgra8888_rgb565.c',
			'src/blend/blend_image_bgra8888_rgba8888.c',
			'src/blend/blend_image_rgb565_bgr565.c',
			'src/blend/blend_image_rgb565_bgra8888.c',
			'src/blend/blend_image_rgb565_rgb565.c',
			'src/blend/blend_image_rgb565_rgba8888.c',
			'src/blend/blend_image_rgb888_bgr565.c',
			'src/blend/blend_image_rgb888_bgra8888.c',
			'src/blend/blend_image_rgb888_rgb565.c',
			'src/blend/blend_image_rgb888_rgb888.c',
			'src/blend/blend_image_rgb888_rgba8888.c',
			'src/blend/blend_image_rgba8888_bgr565.c',
			'src/blend/blend_image_rgba8888_bgra8888.c',
			'src/blend/blend_image_rgba8888_rgb565.c',
			'src/blend/blend_image_rgba8888_rgba8888.c',
			'src/blend/fill_image_abgr8888.c',
			'src/blend/fill_image_argb8888.c',
			'src/blend/fill_image_bgr565.c',
			'src/blend/fill_image_bgr888.c',
			'src/blend/fill_image_bgra8888.c',
			'src/blend/fill_image_rgb565.c',
			'src/blend/fill_image_rgb888.c',
			'src/blend/fill_image_rgba8888.c',
			'src/blend/image_g2d.c',
			'src/blend/rotate_image_bgr565.c',
			'src/blend/rotate_image_bgr888.c',
			'src/blend/rotate_image_bgra8888.c',
			'src/blend/rotate_image_rgb565.c',
			'src/blend/rotate_image_rgb888.c',
			'src/blend/rotate_image_rgba8888.c',
			'src/blend/soft_g2d.c',
			'src/blend/stm32_g2d.c',
			'src/clip_board/clip_board_default.c',
			'src/dialog_highlighters/dialog_highlighter_builtins.c',
			'src/dialog_highlighters/dialog_highlighter_default.c',
			'src/ext_widgets/canvas_widget/canvas_widget.c',
			'src/ext_widgets/color_picker/color_component.c',
			'src/ext_widgets/color_picker/color_picker.c',
			'src/ext_widgets/color_picker/rgb_and_hsv.c',
			'src/ext_widgets/combo_box_ex/combo_box_ex.c',
			'src/ext_widgets/ext_widgets.c',
			'src/ext_widgets/features/draggable.c',
			'src/ext_widgets/file_browser/file_browser.c',
			'src/ext_widgets/file_browser/file_browser_view.c',
			'src/ext_widgets/file_browser/file_chooser.c',
			'src/ext_widgets/gif_image/gif_image.c',
			'src/ext_widgets/guage/guage.c',
			'src/ext_widgets/guage/guage_pointer.c',
			'src/ext_widgets/image_animation/image_animation.c',
			'src/ext_widgets/image_value/image_value.c',
			'src/ext_widgets/keyboard/candidates.c',
			'src/ext_widgets/keyboard/keyboard.c',
			'src/ext_widgets/keyboard/lang_indicator.c',
			'src/ext_widgets/mledit/line_number.c',
			'src/ext_widgets/mledit/mledit.c',
			'src/ext_widgets/mutable_image/mutable_image.c',
			'src/ext_widgets/progress_circle/progress_circle.c',
			'src/ext_widgets/rich_text/rich_text.c',
			'src/ext_widgets/rich_text/rich_text_node.c',
			'src/ext_widgets/rich_text/rich_text_parser.c',
			'src/ext_widgets/rich_text/rich_text_render_node.c',
			'src/ext_widgets/rich_text/rich_text_view.c',
			'src/ext_widgets/scroll_label/hscroll_label.c',
			'src/ext_widgets/scroll_view/children_layouter_list_view.c',
			'src/ext_widgets/scroll_view/list_item.c',
			'src/ext_widgets/scroll_view/list_view.c',
			'src/ext_widgets/scroll_view/list_view_h.c',
			'src/ext_widgets/scroll_view/scroll_bar.c',
			'src/ext_widgets/scroll_view/scroll_view.c',
			'src/ext_widgets/slide_menu/slide_menu.c',
			'src/ext_widgets/slide_view/slide_indicator.c',
			'src/ext_widgets/slide_view/slide_view.c',
			'src/ext_widgets/svg_image/svg_image.c',
			'src/ext_widgets/switch/switch.c',
			'src/ext_widgets/text_selector/text_selector.c',
			'src/ext_widgets/time_clock/time_clock.c',
			'src/font_loader/font_loader_bitmap.c',
			'src/font_loader/font_loader_stb.c',
			'src/graphic_buffer/graphic_buffer_default.c',
			'src/image_loader/image_loader_stb.c',
			'src/input_engines/input_engine_null.c',
			'src/input_methods/input_method_creator.c',
			'src/layouters/children_layouter_builtins.c',
			'src/layouters/children_layouter_default.c',
			'src/layouters/children_layouter_parser.c',
			'src/layouters/self_layouter_builtins.c',
			'src/layouters/self_layouter_default.c',
			'src/layouters/self_layouter_menu.c',
			'src/layouters/self_layouter_parser.c',
			'src/lcd/lcd_mem_bgr565.c',
			'src/lcd/lcd_mem_bgr888.c',
			'src/lcd/lcd_mem_bgra8888.c',
			'src/lcd/lcd_mem_rgb565.c',
			'src/lcd/lcd_mem_rgba8888.c',
			'src/main_loop/main_loop_simple.c',
			'src/native_window/native_window_raw.c',
			'src/svg/bsvg.c',
			'src/svg/bsvg_builder.c',
			'src/svg/bsvg_draw.c',
			'src/svg/bsvg_to_svg.c',
			'src/svg/svg_path.c',
			'src/svg/svg_path_parser.c',
			'src/svg/svg_shape.c',
			'src/svg/svg_to_bsvg.c',
			'src/tkc/asset_info.c',
			'src/tkc/buffer.c',
			'src/tkc/color.c',
			'src/tkc/color_parser.c',
			'src/tkc/compressor.c',
			'src/tkc/crc.c',
			'src/tkc/darray.c',
			'src/tkc/data_reader.c',
			'src/tkc/data_reader_factory.c',
			'src/tkc/data_reader_file.c',
			'src/tkc/data_writer.c',
			'src/tkc/data_writer_factory.c',
			'src/tkc/data_writer_file.c',
			'src/tkc/date_time.c',
			'src/tkc/easing.c',
			'src/tkc/emitter.c',
			'src/tkc/event.c',
			'src/tkc/event_source.c',
			'src/tkc/event_source_fd.c',
			'src/tkc/event_source_idle.c',
			'src/tkc/event_source_manager.c',
			'src/tkc/event_source_manager_default.c',
			'src/tkc/event_source_timer.c',
			'src/tkc/expr_eval.c',
			'src/tkc/fs.c',
			'src/tkc/func_call_parser.c',
			'src/tkc/idle_info.c',
			'src/tkc/idle_manager.c',
			'src/tkc/int_str.c',
			'src/tkc/iostream.c',
			'src/tkc/istream.c',
			'src/tkc/log.c',
			'src/tkc/matrix.c',
			'src/tkc/mem.c',
			'src/tkc/mutex_nest.c',
			'src/tkc/named_value.c',
			'src/tkc/object.c',
			'src/tkc/object_array.c',
			'src/tkc/object_default.c',
			'src/tkc/object_locker.c',
			'src/tkc/ostream.c',
			'src/tkc/path.c',
			'src/tkc/rect.c',
			'src/tkc/ring_buffer.c',
			'src/tkc/rom_fs.c',
			'src/tkc/slist.c',
			'src/tkc/socket_pair.c',
			'src/tkc/str.c',
			'src/tkc/str_str.c',
			'src/tkc/time_now.c',
			'src/tkc/timer_info.c',
			'src/tkc/timer_manager.c',
			'src/tkc/tokenizer.c',
			'src/tkc/utf8.c',
			'src/tkc/utils.c',
			'src/tkc/value.c',
			'src/tkc/value_desc.c',
			'src/tkc/wstr.c',
			'src/ui_loader/ui_binary_writer.c',
			'src/ui_loader/ui_builder_default.c',
			'src/ui_loader/ui_loader_default.c',
			'src/ui_loader/ui_loader_xml.c',
			'src/ui_loader/ui_serializer.c',
			'src/ui_loader/ui_xml_writer.c',
			'src/ui_loader/window_open.c',
			'src/vgcanvas/vgcanvas_nanovg_soft.c',
			'src/widget_animators/widget_animator_factory.c',
			'src/widget_animators/widget_animator_prop.c',
			'src/widget_animators/widget_animator_prop2.c',
			'src/widget_animators/widget_animator_scroll.c',
			'src/widgets/app_bar.c',
			'src/widgets/button.c',
			'src/widgets/button_group.c',
			'src/widgets/calibration_win.c',
			'src/widgets/check_button.c',
			'src/widgets/clip_view.c',
			'src/widgets/color_tile.c',
			'src/widgets/column.c',
			'src/widgets/combo_box.c',
			'src/widgets/combo_box_item.c',
			'src/widgets/dialog_client.c',
			'src/widgets/dialog_helper.c',
			'src/widgets/dialog_title.c',
			'src/widgets/digit_clock.c',
			'src/widgets/dragger.c',
			'src/widgets/edit.c',
			'src/widgets/grid.c',
			'src/widgets/grid_item.c',
			'src/widgets/group_box.c',
			'src/widgets/image.c',
			'src/widgets/label.c',
			'src/widgets/overlay.c',
			'src/widgets/pages.c',
			'src/widgets/popup.c',
			'src/widgets/progress_bar.c',
			'src/widgets/row.c',
			'src/widgets/slider.c',
			'src/widgets/spin_box.c',
			'src/widgets/system_bar.c',
			'src/widgets/tab_button.c',
			'src/widgets/tab_button_group.c',
			'src/widgets/tab_control.c',
			'src/widgets/view.c',
			'src/widgets/widgets.c',
			'src/window_animators/window_animator_builtins.c',
			'src/window_animators/window_animator_center_scale.c',
			'src/window_animators/window_animator_common.c',
			'src/window_animators/window_animator_fade.c',
			'src/window_animators/window_animator_htranslate.c',
			'src/window_animators/window_animator_popdown.c',
			'src/window_animators/window_animator_popup.c',
			'src/window_animators/window_animator_slide.c',
			'src/window_animators/window_animator_slide_down.c',
			'src/window_animators/window_animator_slide_left.c',
			'src/window_animators/window_animator_slide_right.c',
			'src/window_animators/window_animator_slide_up.c',
			'src/window_animators/window_animator_vtranslate.c',
			'src/window_manager/window_manager_default.c',
			'src/xml/xml_builder.c',
			'src/xml/xml_parser.c',
			'src/platforms/raw/cond_var_null.c',
			'src/platforms/raw/fs_os.c',
			'src/platforms/raw/mutex_null.c',
			'src/platforms/raw/semaphore_null.c',
			'src/base/input_device_status.c',
			'src/base/input_engine.c',
			'src/base/input_method.c',

	3. stm32 需要配置：

		① LDTC


	4. rt-thread需要实现：

		/* 获取时间函数 */
		uint64_t get_time_ms64()
		{
			return HAL_GetTick();
		}

		/* 延时函数 */
		void sleep_ms(uint32_t ms)
		{
			rt_thread_mdelay(ms);
		}

		/* 初始化内存， 这块内存是awtk要使用的堆内存 */
		ret_t platform_prepare(void)
		{
			return tk_mem_init((void *)AWTK_MEMBER, AWTK_MEMBER_SIZE);
		}

		/* loop分发输入事件, 事件有 键盘事件、鼠标移动事件、点击事件 */
		/* 循环执行， 间隔10ms */
		uint8_t platform_disaptch_input(main_loop_t *loop)
		{
			tp_dev.scan(0);

			int32_t x = tp_dev.x[0];
			int32_t y = tp_dev.y[0];

			if (tp_dev.sta & TP_PRES_DOWN)
				main_loop_post_pointer_event(loop, TRUE, x, y);
			else
				main_loop_post_pointer_event(loop, FALSE, y, x);

			return 0;
		}

	4
