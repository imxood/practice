# Rust 学习笔记

## Rust 库 收集

    tokio

        https://github.com/tokio-rs/tokio

        功能包括:

        fs	fsAsynchronous file and standard stream adaptation.
        io	Traits, helpers, and type definitions for asynchronous I/O functionality.
        net	TCP/UDP/Unix bindings for tokio.
        prelude	A "prelude" for users of the tokio crate.
        process	processAn implementation of asynchronous process management for Tokio.
        runtime	rtThe Tokio runtime.
        signal	signalAsynchronous signal handling for Tokio
        stream	streamStream utilities for Tokio.
        sync	syncSynchronization primitives for use in asynchronous contexts.
        task	Asynchronous green-threads.
        time	timeUtilities for tracking time.

## Rust 的 安装与卸载

    安装:
        curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh

    版本号:
        rustc --version

    升级:
        rustup update

    使用 不同 版本:
        rustup default stable
        rustup default nightly

    添加工具 cargo-edit:
        cargo install cargo-edit

    卸载:
        rustup self uninstall


## 使用特定的 rust 版本

    参考: https://doc.rust-lang.org/edition-guide/rust-2018/rustup-for-managing-rust-versions.html

    rustup toolchain install nightly-2020-11-19
    rustup toolchain list
    rustup default nightly-2020-11-19

    ps:
        "2020-11-19" 这个时间是在 rust 的 git 中的tag上找的


    # Install the nightly toolchain
    rustup toolchain install nightly
    # Configure your current project to use nightly (run this command within the project)
    rustup override set nightly
    # OR configure cargo to use nightly for all projects -- switch back with `rustup default stable`
    rustup default nightly


## vscode 中 rust 的插件

    1. Rust
    2. Crates
    3. Better TOML
    4. CodeLLDB
    5. rust-analyzer

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

    编译 但不生成 可执行程序:
        cargo check

    运行目标程序 (也可以一步构建项目):
        cargo run

    发布构建:
        cargo build --release

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

## iced: 编译 并 运行所有的 examples

    #!/bin/bash

    examples=(iced_core iced_futures iced_graphics iced_native iced_style iced_glow iced_glutin iced_winit iced_web iced_wgpu bezier_tool iced clock color_palette counter custom_widget download_progress events game_of_life geometry integration pane_grid pick_list pokedex progress_bar qr_code scrollable solar_system stopwatch styling svg todos tour)

    for example in ${examples[@]}; do
        cargo build --verbose --package $example
    done

    for example in ${examples[@]}; do
        echo "start run: cargo run --verbose --package $example"
        cargo run --verbose --package $example
    done


## iced 例子

    学习基本的布局:
        target/debug/pane_grid
        examples/tour

    学习canvas:
        examples/clock

### valora

    cargo new hello_valora --bin && cd hello_valora
    cargo add valora

## cargo 的进一步用法

    cargo new hello_world <--bin>, 创建一个二进制程序
    cargo new hello_world --lib, 创建一个库

    练习:
        git clone https://github.com/rust-lang-nursery/rand.git
        cd rand
        cargo build

## bevy

    git clone https://github.com/bevyengine/bevy
    cargo run --example breakout
