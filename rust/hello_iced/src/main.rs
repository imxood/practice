use iced::{button, Button, Column, Element, Sandbox, Settings, Text};

#[derive(Debug, Clone, Copy)]
pub enum Message {
    Inc,
    Dec,
}

#[derive(Default)]
struct Counter {
    v: i32,
    inc_button: button::State,
    dec_button: button::State,
}

// Command, executor, Application

// impl Application for Counter {
//     type Executor = executor::Default;
//     type Message = ();
//     type Flags = ();

//     fn new(flags: Self::Flags) -> (Self, Command<Self::Message>) {
//         (Self::default(), Command::none())
//     }

//     fn title(&self) -> String {
//         String::from("A cool application")
//     }

//     fn update(&mut self, _message: Self::Message) -> Command<Self::Message> {
//         Command::none()
//     }

//     fn view(&mut self) -> Element<Self::Message> {
//         Text::new("Hello, world!").into()
//     }
// }

impl Sandbox for Counter {
    type Message = Message;

    fn new() -> Self {
        Self::default()
    }

    fn title(&self) -> String {
        String::from("hello, world")
    }

    fn update(&mut self, message: Self::Message) {
        match message {
            Message::Inc => self.v += 1,
            Message::Dec => self.v -= 1,
        }
    }

    fn view(&mut self) -> Element<'_, Self::Message> {
        Column::new()
            .push(Button::new(&mut self.inc_button, Text::new("增加")).on_press(Message::Inc))
            .push(Text::new(&self.v.to_string()).size(50))
            .push(Button::new(&mut self.dec_button, Text::new("减少")).on_press(Message::Dec))
            .into()
    }
}

fn main() {
    Counter::run(Settings::default()).expect("something is wrong");
}
