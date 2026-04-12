import Foundation
import Metal

func readSafeInt(prompt: String, validRange: ClosedRange<Int>) -> Int {
    while true {
        print(prompt, terminator: "")
        guard let input = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines),
              let number = Int(input) else {
            print("Ошибка: Введите корректное целое число.")
            continue
        }
        
        if validRange.contains(number) {
            return number
        } else {
            print("Ошибка: Число должно быть в диапазоне от \(validRange.lowerBound) до \(validRange.upperBound).")
        }
    }
}

func readSafeFloat(prompt: String) -> Float {
    while true {
        print(prompt, terminator: "")
        guard let input = readLine()?
                .trimmingCharacters(in: .whitespacesAndNewlines)
                .replacingOccurrences(of: ",", with: "."),
              let number = Float(input) else {
            print("Ошибка: Введите корректное число (например, 2.5 или 2,5).")
            continue
        }
        return number
    }
}

func exactIntegralVariant1(a: Float, b: Float) -> Float {
    func F(_ x: Float) -> Float {
        return (pow(x, 4) / 4.0) - (pow(x, 3)) + 3.5 * pow(x, 2) - 10 * x
    }
    return F(b) - F(a)
}

guard let device = MTLCreateSystemDefaultDevice(),
      let commandQueue = device.makeCommandQueue(),
      let library = device.makeDefaultLibrary() else {
    fatalError("Ошибка: GPU не найден или Metal не поддерживается.")
}

func computeOnGPU(method: String, a: Float, b: Float, n: Int, funcId: Int) -> Float {
    guard let function = library.makeFunction(name: method),
          let pipeline = try? device.makeComputePipelineState(function: function) else {
        fatalError("Шейдер \(method) не найден в файле .metal!")
    }
    
    let threadCount = (method == "simpson") ? n / 2 : n
    let h = (b - a) / Float(n)
    
    var a_ref = a
    var h_ref = h
    var f_id = Int32(funcId)
    
    let bufferSize = threadCount * MemoryLayout<Float>.stride
    guard let resultsBuffer = device.makeBuffer(length: bufferSize, options: .storageModeShared),
          let commandBuffer = commandQueue.makeCommandBuffer(),
          let encoder = commandBuffer.makeComputeCommandEncoder() else {
        return 0.0
    }
    
    encoder.setComputePipelineState(pipeline)
    encoder.setBuffer(resultsBuffer, offset: 0, index: 0)
    encoder.setBytes(&a_ref, length: MemoryLayout<Float>.size, index: 1)
    encoder.setBytes(&h_ref, length: MemoryLayout<Float>.size, index: 2)
    encoder.setBytes(&f_id, length: MemoryLayout<Int32>.size, index: 3)
    
    let gridSize = MTLSize(width: threadCount, height: 1, depth: 1)
    let groupSize = MTLSize(width: min(threadCount, pipeline.maxTotalThreadsPerThreadgroup), height: 1, depth: 1)
    
    encoder.dispatchThreads(gridSize, threadsPerThreadgroup: groupSize)
    encoder.endEncoding()
    commandBuffer.commit()
    commandBuffer.waitUntilCompleted()
    
    let pointer = resultsBuffer.contents().bindMemory(to: Float.self, capacity: threadCount)
    let bufferPointer = UnsafeBufferPointer(start: pointer, count: threadCount)
    return bufferPointer.reduce(0, +)
}

func runIntegration(methodName: String, methodShader: String, a: Float, b: Float, eps: Float, k: Float, funcId: Int) -> (name: String, value: Float, n: Int, err: Float) {
    let tableWidth = 76
    let separator = String(repeating: "=", count: tableWidth)
    let thinSeparator = String(repeating: "-", count: tableWidth)
    
    print("\n" + separator)
    let paddingSize = max(0, (tableWidth - methodName.count) / 2)
    let centerPadding = String(repeating: " ", count: paddingSize)
    print("\(centerPadding)\(methodName.uppercased())")
    print(separator)
    
    print(String(format: "%-12@ | %-12@ | %@", " Шаг (n)" as NSString, " Интеграл" as NSString, " Погрешность" as NSString))
    print(thinSeparator)
    
    var n = 4
    var I0 = computeOnGPU(method: methodShader, a: a, b: b, n: n, funcId: funcId)
    print(String(format: " %10d | %12.5f | %@", n, I0, " -" as NSString))
    
    let maxN = 16_777_216
    
    while true {
        n *= 2
        
        if n > maxN {
            print(separator)
            print(String(format: "ОСТАНОВКА: Достигнут лимит памяти (n=%d).", n))
            return (methodName, I0, n, -1.0)
        }
        
        let I1 = computeOnGPU(method: methodShader, a: a, b: b, n: n, funcId: funcId)
        let error = abs(I1 - I0) / (pow(2.0, k) - 1.0)
        
        if n <= 1024 || n % 16384 == 0 {
            print(String(format: " %10d | %12.5f |  %.6e", n, I1, error))
        }
        
        if error <= eps {
            print(separator)
            print(String(format: "ИТОГ: Интеграл = %.5f | Шагов = %d | Погрешность = %.6e", I1, n, error))
            return (methodName, I1, n, error)
        }
        I0 = I1
    }
}

print("=== Лабораторная работа №3. Численное интегрирование (GPU Metal) ===")
print("Доступные функции:")
print("1. f(x) = x^3 - 3x^2 + 7x - 10 (Вариант 10)")
print("2. f(x) = sin(x)")
print("3. f(x) = 1/x")
print("4. f(x) = sin(100x) * exp(-x^2) (Осциллятор)")
print("5. f(x) = Сумма(1..100) sin(x*i)*cos(x/i) (Убийца CPU)")

let funcId = readSafeInt(prompt: "\nВведите номер функции (1-5): ", validRange: 1...5)
let a = readSafeFloat(prompt: "Введите предел a: ")
var b = readSafeFloat(prompt: "Введите предел b: ")

while a >= b {
    print("Ошибка: Верхний предел (b) должен быть строго больше нижнего (a).")
    b = readSafeFloat(prompt: "Введите предел b заново: ")
}

var eps = readSafeFloat(prompt: "Введите точность (например, 0.001): ")
while eps <= 0.0 {
    print("Ошибка: Точность должна быть строго положительным числом.")
    eps = readSafeFloat(prompt: "Введите точность заново: ")
}

print("\nЗапуск параллельных вычислений на \(device.name)...\n")

if funcId == 1 {
    let exact = exactIntegralVariant1(a: a, b: b)
    print("Точное аналитическое значение (Ньютон-Лейбниц): \(String(format: "%.5f", exact))\n")
}

var resultsData: [(name: String, value: Float, n: Int, err: Float)] = []

let startTime = CFAbsoluteTimeGetCurrent()

resultsData.append(runIntegration(methodName: "Левые прямоугольники",  methodShader: "left_rect",  a: a, b: b, eps: eps, k: 1.0, funcId: funcId))
resultsData.append(runIntegration(methodName: "Правые прямоугольники", methodShader: "right_rect", a: a, b: b, eps: eps, k: 1.0, funcId: funcId))
resultsData.append(runIntegration(methodName: "Средние прямоугольники",methodShader: "mid_rect",   a: a, b: b, eps: eps, k: 2.0, funcId: funcId))
resultsData.append(runIntegration(methodName: "Метод трапеций",        methodShader: "trapezoid",  a: a, b: b, eps: eps, k: 2.0, funcId: funcId))
resultsData.append(runIntegration(methodName: "Метод Симпсона",        methodShader: "simpson",    a: a, b: b, eps: eps, k: 4.0, funcId: funcId))

let endTime = CFAbsoluteTimeGetCurrent()
let totalTime = endTime - startTime

print("\n")
let tableWidth = 76
let separator = String(repeating: "=", count: tableWidth)
let thinSeparator = String(repeating: "-", count: tableWidth)

print(separator)
print("                       СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
print(separator)

let headerName = "Метод".padding(toLength: 24, withPad: " ", startingAt: 0)
print("\(headerName) | Интеграл   | Шагов (n)  | Погрешность")
print(thinSeparator)

for res in resultsData {
    let nameStr = res.name.padding(toLength: 24, withPad: " ", startingAt: 0)
    let errStr = res.err < 0 ? "ПРЕВЫШЕН ЛИМИТ" : String(format: "%.6e", res.err)
    print(String(format: "%@ | %10.5f | %10d | %@", nameStr, res.value, res.n, errStr))
}
print(separator)

print(String(format: "Общее время вычислений: %.4f сек", totalTime))
print("\nВычисления успешно завершены.")
