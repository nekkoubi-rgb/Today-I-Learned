package JavaSilver; //パッケージ宣言

import java.util.Scanner; //Scannerクラスのインポート(キーボード入力)

public class TenNumbers { //クラス宣言
    public static void main(String[] args) { //mainメソッドの宣言
        Scanner sc = new Scanner(System.in); //Scannerオブジェクトの生成
        int[] arr = new int[10]; //int型配列arrを10個分作成

        for (int i = 0; i < 10; i++) { //iを0から9まで繰り返す
            int val; //入力値を格納する変数の宣言
            while (true) {//breakするまで無限ループ
                System.out.print("項目 " + (i + 1) + " の値 (0-99): "); //項目 x の値 (0-99): を表示　0-99はマジックナンバーの為、MAX_VALUE等に置き換えると◎
                String line = sc.nextLine().trim(); //nextLine()で文字列として1行取得し、trim()で前後の空白を削除。
                try { //例外処理(一周)
                    val = Integer.parseInt(line); //Integer=数字に関するクラス。parseInt=文字列(line)をint型に変換するメソッド。
                    if (val < 0 || val > 99) {
                        System.out.println("0から99の整数を入力してください。"); //MIN_VALUEからMAX_VALUEの～。にする
                        continue;
                    }
                    break;
                } catch (NumberFormatException e) { //tryの実行中にエラーが発生した場合に実行
                    System.out.println("整数を入力してください。");
                }
            }
            arr[i] = val;
        }

        System.out.println("\n入力された一覧:");
        for (int i = 0; i < 10; i++) {
            System.out.println((i + 1) + ": " + arr[i]);
        }

        sc.close();
    }
}
