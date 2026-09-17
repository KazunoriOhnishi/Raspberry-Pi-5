#include <chrono>
#include <thread>
#include <iostream>
#include <gpiod.h>

int main() {
    const char* chip_path = "/dev/gpiochip0";
    const unsigned int gpio = 17;       // ← 点滅させたい GPIO 番号（BCM）
    const unsigned int offsets[1] = { gpio };

    // --- 出力設定（v2 API 必須の最小構成） ---
    gpiod_line_settings* settings = gpiod_line_settings_new();
    gpiod_line_settings_set_direction(settings, GPIOD_LINE_DIRECTION_OUTPUT);
    gpiod_line_settings_set_output_value(settings, GPIOD_LINE_VALUE_INACTIVE);

    gpiod_line_config* line_cfg = gpiod_line_config_new();
    gpiod_line_config_add_line_settings(line_cfg, offsets, 1, settings);

    gpiod_request_config* req_cfg = gpiod_request_config_new();
    gpiod_request_config_set_consumer(req_cfg, "blink-led");

    // --- GPIO17 を出力としてリクエスト ---
    gpiod_chip* chip = gpiod_chip_open(chip_path);
    gpiod_line_request* req =
        gpiod_chip_request_lines(chip, req_cfg, line_cfg);

    if (!req) {
        std::cerr << "GPIO" << gpio << " のリクエストに失敗しました\n";
        return 1;
    }

    std::cout << "GPIO" << gpio << " を点滅させます。Ctrl+Cで終了\n";

    int n =0;

    // --- 点滅ループ（最短） ---
    while (true) {
        gpiod_line_request_set_value(req, gpio, GPIOD_LINE_VALUE_ACTIVE);
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));

        gpiod_line_request_set_value(req, gpio, GPIOD_LINE_VALUE_INACTIVE);
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));

        n++;
        printf("n= %d\n", n);

    }

    // ここには来ないが一応
    gpiod_line_request_release(req);
    gpiod_chip_close(chip);

    return 0;
}
