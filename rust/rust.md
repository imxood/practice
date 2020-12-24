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

### valora

    cargo new hello_valora --bin && cd hello_valora
    cargo add valora
