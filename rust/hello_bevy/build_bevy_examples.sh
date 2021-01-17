#!/bin/bash

# custom_loop ecs_guide headless headless_wasm

examples=(3d_scene android array_texture asset_loading assets_wasm audio bevymark breakout button change_detection char_input_events clear_color contributors custom_asset custom_asset_io custom_diagnostic drag_and_drop empty empty_defaults event fixed_timestep font_atlas_debug gamepad_input gamepad_input_events generic_reflection hello_wasm hello_world hierarchy hot_asset_reloading hot_shader_reloading keyboard_input keyboard_input_events load_gltf log_diagnostics logs mesh_custom_attribute mouse_input mouse_input_events msaa multiple_windows parallel_query parenting plugin plugin_group reflection reflection_types removal_detection return_after_run scale_factor_override scene shader_custom_material shader_defs spawner sprite sprite_sheet startup_system state system_chaining text text2d text_debug texture texture_atlas thread_pool_resources timers touch_input touch_input_events trait_reflection ui update_gltf_scene window_settings winit_wasm z_sort_debug)

for example in ${examples[@]}; do
    cargo run --example $example
done
