import {createWorker, OEM} from 'tesseract.js';
import {resolve} from 'node:path';
const fixture=resolve(process.argv[2] || '../docs/service/images/22-receipt-upload.png');
const worker=await createWorker('jpn',OEM.LSTM_ONLY,{langPath:resolve('public/ocr'),cacheMethod:'none'});
try {
 const {data}=await worker.recognize(fixture);
 const japaneseCharacters=(data.text.match(/[\u3040-\u30ff\u3400-\u9fff]/g)||[]).length;
 const result={scope:'Node Tesseract Japanese engine/model smoke; generated UI fixture, not browser or receipt accuracy acceptance',fixture:fixture.split('/').at(-1),recognizedCharacters:data.text.length,japaneseCharacters,passed:japaneseCharacters>20};
 process.stdout.write(JSON.stringify(result,null,2)+'\n');
 if(!result.passed)process.exitCode=1;
} finally {await worker.terminate();}
