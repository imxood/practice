use std::time::Duration;

extern crate libusb;

fn main() {
    let mut context = libusb::Context::new().unwrap();

    for mut device in context.devices().unwrap().iter() {
        let device_desc = device.device_descriptor().unwrap();
        if device_desc.vendor_id() == 0x1234 && device_desc.product_id() == 0x1234 {
            println!(
                "Bus {:03} Device {:03} ID 0x{:04x}:0x{:04x}",
                device.bus_number(),
                device.address(),
                device_desc.vendor_id(),
                device_desc.product_id()
            );
            for index in device_desc.num_configurations() {
                let config_desc = device.config_descriptor(index).unwrap();
                for iface in config_desc.interfaces() {
                    iface.
                }
            }

            let mut handle = device.open().unwrap();
            println!("Device Opened");

            let iface = 0;

            let ret = handle.kernel_driver_active(iface).unwrap();
            if ret {
                println!("Kernel Driver Active");
                handle.detach_kernel_driver(iface).unwrap();
                println!("Kernel Driver Detached");
            }
            handle.claim_interface(iface).unwrap();
            println!("Claim Interface!");

            let mut endpoint = 0x01;
            let buf = [0x01, 0x02, 0x03, 0x04];

            let size = handle
                .write_bulk(endpoint, &buf[..], Duration::from_secs(5))
                .unwrap();
            println!("Write successful, write size: {}", size);

            handle.release_interface(iface).unwrap();
            println!("Released Interface!");
        }
    }
}
