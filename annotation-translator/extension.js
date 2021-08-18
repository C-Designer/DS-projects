const vscode = require('vscode');
const spawn = require('child_process').spawn;
const path = require('path')
const clipboardy = require("clipboardy");

/**
 * @param {vscode.ExtensionContext} context
 */
 function activate(context) {
	
	let disposable = vscode.commands.registerCommand('annotation-translator.translate', async function () { // 비동기 함수

		const editor = vscode.window.activeTextEditor;  // 활성화된 파일문단에 접근가능한 api
		const text = editor.document.getText()  // 파일 텍스트 받아오기
		const result = spawn('python', [path.join(__dirname, 'model/func.py'), text]); // JS와 Py파일연동 & 경로 받아오기 => __dirname

		result.stdout.on('data', async (data)=>{          // py파일에 텍스트값을 던져 매핑된 값을 받는 구조
			const articles = eval("("+data.toString()+")"); // py파일에서 json text값으로 반환 & 이 값을json object로 변환
			const chkbox = [];
			for(var i in articles){   // json object를 array에 저장
				const article = {
					label: articles[i]['detail'],
					detail: articles[i]['label']
				}

				chkbox[i] = article;
			}

			const article = await vscode.window.showQuickPick(chkbox, {   // 매핑된 값들을 리스트로 뿌려 선택할수 있게끔
				matchOnDetail: true
			})
			if (article == null) return     // 선택한 값 없을시 무효

			clipboardy.write(article.label) // 선택한 값을 클립보드에 복사
		})

		result.stderr.on('data', function(data){
			console.log(data.toString());
		})

	});

	context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
	activate,
	deactivate
}
