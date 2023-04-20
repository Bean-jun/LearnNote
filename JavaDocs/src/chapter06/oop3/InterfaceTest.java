package chapter06.oop3;

// 接口
interface Usb {
    // 接口方法
    public abstract void comin();

    // 接口方法
    public abstract void comout();
}

// 接口的继承
interface UsbA extends Usb {
    public abstract String getUsbA();
}

// 接口的继承
interface UsbB extends Usb {
    public abstract String getUsbB();
}

// 接口的继承
interface UsbC extends Usb {
    public abstract String getUsbC();
}

// 接口的多继承
interface SuperUsb extends UsbA, UsbB, UsbC {

}

// 实现UsbA的接口
class Phone implements UsbA {

    @Override
    public void comin() {
        System.out.println("我是手机，插入了USB");
    }

    @Override
    public void comout() {
        System.out.println("我是手机，弹出了USB");
    }

    @Override
    public String getUsbA() {
        return "Phone A";
    }

}

// 继承Phone类，实现UsbC接口
class SmartPhone extends Phone implements UsbC {

    @Override
    public String getUsbC() {
        return "SmartPhone C";
    }

}

class Computer {
    public void link(Usb usb) {
        System.out.println("---连接电脑中----");
        usb.comin();
        usb.comout();
        System.out.println("----断开电脑连接----");
    }
}

public class InterfaceTest {
    public static void main(String[] args) {
        Phone p = new Phone();
        p.comin();
        p.comout();

        SmartPhone p2 = new SmartPhone();
        p2.comin();
        p2.comout();
        System.out.println(p2.getUsbA());
        System.out.println(p2.getUsbC());

        // 接口的多态性
        UsbA p3 = new Phone();
        System.out.println(p3.getUsbA());

        Computer c = new Computer();
        c.link(p);
        c.link(p2);
    }
}
