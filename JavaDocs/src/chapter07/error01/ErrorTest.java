package chapter07.error01;

public class ErrorTest{

    public String[] names = new String[]{"tom", "jerry"};
    public static void main(String[] args) {
        ErrorTest e1 = new ErrorTest();
        try {
            System.out.println(e1.names[10]);
        } catch(ArrayIndexOutOfBoundsException e){
            System.out.println(e);
        }catch(Exception e){
            System.out.println(e);
        }finally{
            System.out.println("finally");
        }
    }
}