mod front_of_house;
mod back_of_order;

// pub use crate::front_of_house::hosting;

fn serve_order() {}

pub fn eat_at_restaurant() {
    // Absolute path
    crate::front_of_house::hosting::add_to_waitlist();

    // Relative path
    front_of_house::hosting::add_to_waitlist();

    let mut meal = back_of_order::Breakfast::summer("Rye");
    println!("meal: {}", meal.toast);
    println!("meal: {}", meal.toast);
}
