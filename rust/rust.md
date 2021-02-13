# Rust 学习笔记

## Rust 的 安装与卸载

    参考链接:
        https://www.rust-lang.org/zh-CN/tools/install

    安装:
        curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh

    版本号:
        rustc --version

    升级:
        rustup update stable
        rustup update

    使用 不同 版本:
        rustup default stable
        rustup default nightly

    添加工具:
        cargo install cargo-edit
        cargo install mdbook

    卸载:
        rustup self uninstall


## 使用特定的 rust 版本

    参考: https://doc.rust-lang.org/edition-guide/rust-2018/rustup-for-managing-rust-versions.html

    rustup toolchain install nightly-2020-11-19
    rustup toolchain list
    rustup default nightly-2020-11-19

    ps:
        "2020-11-19" 这个时间是在 rust 的 git 中的tag上找的

    # 安装 nightly 版本的工具链
    rustup toolchain install nightly

    # 对当前项目使用 nightly
    rustup override set nightly

    # 对所有项目使用 nightly
    rustup default nightly


## vscode 中 rust 的插件

    1. rust-analyzer
    2. Crates
    3. Better TOML
    4. CodeLLDB

## Rust hello_world

    编写点一个程序:
        vim main.rs

        fn main() {
            println!("Hello, world!");
        }

    编译:
        rustc main.rs

    运行:
        ./main

## 使用 Cargo 创建项目

    创建项目 hello_cargo:
        cargo new hello_cargo

    cd hello_cargo

    编译 并生成可执行程序:
        cargo build
        cargo build --release

    编译 但不生成 可执行程序:
        cargo check

    运行目标程序 (也可以一步构建项目):
        cargo run

    创建:
        cargo new hello_world <--bin>, 创建一个二进制程序
        cargo new hello_world --lib, 创建一个库


## 库

    kurbo
        曲线工具

    lyon
        路径细分库, 可以用于基于GPU的2D图形渲染


    tokio

        https://github.com/tokio-rs/tokio

## GUI 开发

### iced

    sudo apt install libssl-dev

    官方的例子:

        git clone https://github.com/hecrj/iced.git

        cd iced

        cargo build

        // --features glow,glow_canvas
        cargo run --package todos

    // 如果无法运行, 就安装下面的软件包
    sudo apt install libvulkan1 mesa-vulkan-drivers vulkan-utils

### iced: 编译 并 运行所有的 examples

    #!/bin/bash

    examples=(iced_core iced_futures iced_graphics iced_native iced_style iced_glow iced_glutin iced_winit iced_web iced_wgpu bezier_tool iced clock color_palette counter custom_widget download_progress events game_of_life geometry integration pane_grid pick_list pokedex progress_bar qr_code scrollable solar_system stopwatch styling svg todos tour)

    for example in ${examples[@]}; do
        cargo build --verbose --package $example
    done

    for example in ${examples[@]}; do
        echo "start run: cargo run --verbose --package $example"
        cargo run --verbose --package $example
    done


### iced 例子

    学习基本的布局:
        target/debug/pane_grid
        examples/tour

    学习canvas:
        examples/clock


### bevy, 游戏引擎

    git clone https://github.com/bevyengine/bevy
    cargo run --example breakout

## libusb, usb库

    在windows上找不到libusb库, 在 ~/.cargo/config 中添加:

    [target.x86_64-pc-windows-msvc.'usb-1.0']
    rustc-link-search = ['D:\libs\64bit']
    rustc-link-lib = ['libusb-1.0']
