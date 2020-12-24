use winit::{
    dpi::LogicalSize,
    error::OsError,
    event::{Event, WindowEvent},
    event_loop::{ControlFlow, EventLoop},
    window::Window,
    window::WindowBuilder,
};

pub const WINDOW_NAME: &str = "Hello Winit";

#[derive(Debug)]
pub struct WinitState {
    pub event_loop: EventLoop<()>,
    pub window: Window,
}

impl WinitState {
    pub fn new<T: Into<String>>(title: T, size: LogicalSize<i32>) -> Result<Self, OsError> {
        let event_loop = EventLoop::new();
        let result = WindowBuilder::new()
            .with_title(title)
            .with_inner_size(size)
            .build(&event_loop);
        result.map(|window| Self { event_loop, window })
    }
}

impl Default for WinitState {
    fn default() -> Self {
        Self::new(
            WINDOW_NAME,
            LogicalSize {
                width: 800,
                height: 600,
            },
        )
        .expect("Could not create a window")
    }
}

fn main() {
    let winit_state = WinitState::default();

    winit_state.event_loop.run(move |event, target, control_flow| {
        // *control_flow = ControlFlow::Poll; // This is ideal for games and similar applications
        *control_flow = ControlFlow::Wait; // This is ideal for non-game applications

        match event {
            Event::WindowEvent {
                event: WindowEvent::CloseRequested,
                ..
            } => {
                println!("The close button wased pressed; stopping!");
                *control_flow = ControlFlow::Exit;
            },
            Event::MainEventsCleared => {
                // target.request_redraw();
                // winit_state.window.request_redraw();
            },
            Event::RedrawRequested(_) => {

            },
            _ => {}
        }
    });

    // event_loop.run(move |event, _, control_flow| {
    //     // ControlFlow::Poll continuously runs the event loop, even if the OS hasn't
    //     // dispatched any events. This is ideal for games and similar applications.
    //     *control_flow = ControlFlow::Poll;

    //     // ControlFlow::Wait pauses the event loop if no events are available to process.
    //     // This is ideal for non-game applications that only update in response to user
    //     // input, and uses significantly less power/CPU time than ControlFlow::Poll.
    //     *control_flow = ControlFlow::Wait;

    //     match event {
    //         Event::WindowEvent {
    //             event: WindowEvent::CloseRequested,
    //             ..
    //         } => {
    //             println!("The close button was pressed; stopping");
    //             *control_flow = ControlFlow::Exit
    //         }
    //         Event::MainEventsCleared => {
    //             // Application update code.

    //             // Queue a RedrawRequested event.
    //             //
    //             // You only need to call this if you've determined that you need to redraw, in
    //             // applications which do not always need to. Applications that redraw continuously
    //             // can just render here instead.
    //             window.request_redraw();
    //         }
    //         Event::RedrawRequested(_) => {
    //             // Redraw the application.
    //             //
    //             // It's preferable for applications that do not render continuously to render in
    //             // this event rather than in MainEventsCleared, since rendering in here allows
    //             // the program to gracefully handle redraws requested by the OS.
    //         }
    //         _ => (),
    //     }
    // });
}
