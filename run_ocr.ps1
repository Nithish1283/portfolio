Add-Type -AssemblyName System.Drawing
$code = @"
using System;
using System.IO;
using System.Threading.Tasks;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;
using Windows.Storage;
using Windows.Storage.Streams;

public class WinOcr {
    public static async Task<string> OcrFile(string path) {
        StorageFile file = await StorageFile.GetFileFromPathAsync(path);
        using (IRandomAccessStream stream = await file.OpenAsync(FileAccessMode.Read)) {
            BitmapDecoder decoder = await BitmapDecoder.CreateAsync(stream);
            SoftwareBitmap bitmap = await decoder.GetSoftwareBitmapAsync();
            OcrEngine engine = OcrEngine.TryCreateFromLanguage(new Windows.Globalization.Language("en-US"));
            OcrResult result = await engine.RecognizeAsync(bitmap);
            return result.Text;
        }
    }
}
"@

Add-Type -TypeDefinition $code -Language CSharp
Get-ChildItem cert_*.png | ForEach-Object {
    Write-Host "=== $($_.Name) ==="
    $task = [WinOcr]::OcrFile($_.FullName)
    $task.Wait()
    Write-Host $task.Result
}
