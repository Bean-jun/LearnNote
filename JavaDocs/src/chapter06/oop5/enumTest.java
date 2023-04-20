package chapter06.oop5;

// 枚举类的定义方法
enum Score {
    A("优秀", 90),
    B("良好", 80),
    C("及格", 60);

    // 配置当前枚举对象中包含的字段
    private final String desc;
    private final int code;

    public String getDesc() {
        return desc;
    }

    public int getCode() {
        return code;
    }

    // 私有化构造器
    private Score(String desc, int code) {
        this.desc = desc;
        this.code = code;
    }
}

public class enumTest {
    public static void main(String[] args) {
        System.out.println(Score.A);
        System.out.println(Score.A.getDesc());

        // valueof 返回当前枚举类的对象
        Score x = Score.valueOf("A");
        System.out.println(x.getDesc() + x.getCode());

        // values返回枚举类型的数组
        Score[] xx = Score.values();
        for (int i = 0; i < xx.length; i++) {
            System.out.println(xx[i].getDesc() + xx[i].getCode());
        }
    }
}
