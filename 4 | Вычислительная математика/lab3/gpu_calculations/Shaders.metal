#include <metal_stdlib>
using namespace metal;

inline float f(int func_id, float x) {
    if (func_id == 1) {
        return pow(x, 3.0) - 3.0 * pow(x, 2.0) + 7.0 * x - 10.0;
    }
    else if (func_id == 2) {
        return sin(x);
    }
    else if (func_id == 3) {
        return 1.0 / x;
    }
    else if (func_id == 4) {
        return sin(100.0 * x) * exp(-pow(x, 2.0));
    }
    else if (func_id == 5) {
        float res = 0.0;
        for (int i = 1; i <= 100; i++) {
            res += sin(x * (float)i) * cos(x / (float)i);
        }
        return res;
    }
    return 0.0;
}



kernel void left_rect(device float* results [[buffer(0)]],
                      constant float& a [[buffer(1)]],
                      constant float& h [[buffer(2)]],
                      constant int& func_id [[buffer(3)]],
                      uint id [[thread_position_in_grid]])
{
    float x = a + id * h;
    results[id] = f(func_id, x) * h;
}

kernel void right_rect(device float* results [[buffer(0)]],
                       constant float& a [[buffer(1)]],
                       constant float& h [[buffer(2)]],
                       constant int& func_id [[buffer(3)]],
                       uint id [[thread_position_in_grid]])
{
    float x = a + (id + 1) * h;
    results[id] = f(func_id, x) * h;
}

kernel void mid_rect(device float* results [[buffer(0)]],
                     constant float& a [[buffer(1)]],
                     constant float& h [[buffer(2)]],
                     constant int& func_id [[buffer(3)]],
                     uint id [[thread_position_in_grid]])
{
    float x = a + (id + 0.5) * h;
    results[id] = f(func_id, x) * h;
}

kernel void trapezoid(device float* results [[buffer(0)]],
                      constant float& a [[buffer(1)]],
                      constant float& h [[buffer(2)]],
                      constant int& func_id [[buffer(3)]],
                      uint id [[thread_position_in_grid]])
{
    float x0 = a + id * h;
    float x1 = a + (id + 1) * h;
    results[id] = (f(func_id, x0) + f(func_id, x1)) / 2.0 * h;
}

kernel void simpson(device float* results [[buffer(0)]],
                    constant float& a [[buffer(1)]],
                    constant float& h [[buffer(2)]],
                    constant int& func_id [[buffer(3)]],
                    uint id [[thread_position_in_grid]])
{
    float x0 = a + (2 * id) * h;
    float x1 = a + (2 * id + 1) * h;
    float x2 = a + (2 * id + 2) * h;
    results[id] = (h / 3.0) * (f(func_id, x0) + 4.0 * f(func_id, x1) + f(func_id, x2));
}
