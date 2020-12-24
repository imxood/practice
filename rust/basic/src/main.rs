#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    // 引用
    let x = 5;

    // x = 6; // 错误用法
    println!("the value is: {}", x);

    // mut 可变变量, 对于 mut, 可以手动添加, 也可以根据'='后面推导类型得到, 比如 可变引用
    let mut y = 5;
    println!("the value is: {}", y);

    y = 6;
    println!("the value is: {}", y);

    let spaces = "   ";
    // 再次使用let: 隐藏前一个变量
    let spaces = spaces.len();

    println!("length: {}", spaces);

    // 声明数据类型
    let guess: u32 = "42".parse().expect("Not a number!");
    println!("guess: {}", guess);

    let sum = 5 + 10;
    println!("sum: {}", sum);

    let a = 15;
    let a = 0b1111;
    let a = 0o17;
    let a = 0xF;
    println!("a: {}", a);

    // 整型
    let i: i8 = 1;
    let i: i16 = 1;
    let i: i32 = 1;
    let i: i64 = 1;
    let i: i128 = 1;
    let i: isize = 1;

    let i: u8 = 1;
    let i: u16 = 1;
    let i: u32 = 1;
    let i: u64 = 1;
    let i: u128 = 1;
    let i: usize = 1;

    // 浮点型
    let f: f32;
    let f: f64;

    // bool 类型
    let flag: bool = false;
    println!("flag: {}", flag);

    // 字符类型, Unicode
    let ch = '哈';
    println!("ch: {}, len: {}", ch, ch.len_utf8());

    /* 复合类型 */

    // 数组
    let a = [1, 2, 3, 4, 5];

    // 元组、解构

    let tup: (i32, f64, u8) = (500, 6.4, 1);
    let x = tup.0;
    let y = tup.0;
    let z = tup.0;

    let (x, y, z): (i32, f64, u8) = (500, 6.4, 1);

    let s1 = String::from("hello"); // 分配内存, 并借用
                                    // s1.push_str(", world"); 错误用法, 此处只是借用, 只能使用, 但不能修改

    let s2 = String::from("hello"); // 移动, s1失效, s2有效
    let s3 = s2.clone(); // 克隆, 全新的一块内存

    take_ownership(s3); // s3 的作用域移动到函数内
                        // s3 在此处已经无效

    {
        let s1 = String::from("hello");
    } // s1 只在作用域内有效, 离开失效 --> 资源获取即初始化

    let s4 = give_ownership(); // give_ownership 将返回值移给 s4
    let s5 = take_and_give_ownership(s4); // s4 传递进去, 并返回, 再移动给s5, s4已失效

    let o1 = calculate_length_1(s5); // 参数的传递: 移动
    println!("string: {}, length: {}", o1.0, o1.1);

    let len = calculate_length_2(&o1.0); // 参数的传递: 引用, 允许使用, 但是不获取所有权
                                         // 离开引用的作用域, 不释放引用值的内存
                                         //  引用 (referencing) --> 借用 (borrowing)
    println!("string: {}, length: {}", o1.0, len);

    let mut s6 = String::from("hello"); // 可变引用
    {
        let r1 = &mut s6;
        // let r2 = &mut s6; // 只能存在一个 s6 的 可变引用
    } // 此处 r1 离开了作用域, 可以创建新的可变引用了

    let r2 = &mut s6; // 唯一的可变引用
    r2.push_str(", world");
    // let r3 = &s6; // r3 和 r2 不能同事拥有所有权

    let r4 = &r2; // r4 是对r2的引用, 相当于转租, 只拥有了使用权
    println!("string: {}", r2);
    println!("string: {}", r4);

    // 切片
    let r5 = &r4[0..5];

    println!("string: {}", r5);
    println!("string: {}", r4);

    let len = 2;
    let r6 = &r4[0..len];
    println!("string: {}", r6);

    // 结构体
    let rect = Rectangle {
        width: 10,
        height: 20,
    };
    println!("rect: {:#?}", rect);
    println!("area: {}", rect.area());

    // trait 和 泛型

    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest(&number_list);
    println!("The largest number is {}", result);

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest(&char_list);
    println!("The largest char is {}", result);
}

fn take_ownership(some_string: String) {
    // some_string 进入作用域
    println!("{}", some_string);
} // some_string 移出作用域, 并调用 'drop' 函数, 占用的内存释放

fn give_ownership() -> String {
    let some_string = String::from("hello");
    some_string
} // 返回 some_string, 内存不释放

fn take_and_give_ownership(some_string: String) -> String {
    some_string
} // 传递进去, 并返回回去

fn calculate_length_1(s: String) -> (String, usize) {
    let length = s.len();
    (s, length)
}

fn calculate_length_2(s: &String) -> usize {
    s.len()
} // s 离开了作用域, 但它并不拥有引用值的所有权, 所以不释放引用值的内存

// PartialOrd 用于比较
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];
    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }
    largest
}
