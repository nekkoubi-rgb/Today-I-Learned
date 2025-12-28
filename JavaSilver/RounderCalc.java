package JavaSilver;

public class RounderCalc {
    public static void main(String[] args) {
        // --- 1. 変数の宣言と代入（Java Silver 2章の基本） ---
        int storeCount = 8;          // 今日回った店舗数（整数型）
        double totalHours = 6.5;    // 総労働時間（浮動小数点型）
        final int HOURLY_PAY = 1200; // 時給（定数：途中で変えられない）

        // --- 2. 計算（算術演算） ---
        // 1時間あたりの平均訪問店舗数
        double storesPerHour = storeCount / totalHours;

        // 今日の概算給与
        double totalSalary = totalHours * HOURLY_PAY;

        // --- 3. 結果の表示 ---
        System.out.println("=== 本日の業務レポート ===");
        System.out.println("訪問店舗数: " + storeCount + " 店");
        System.out.println("労働時間: " + totalHours + " 時間");
        System.out.println("---------------------------");
        System.out.println("1時間あたりの効率: " + storesPerHour + " 店/h");
        System.out.println("本日の概算報酬: " + (int)totalSalary + " 円"); 
    }
}
