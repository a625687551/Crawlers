const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");  //操作节点的函数，比如判断节点类型，生成新的节点等:
const generator = require("@babel/generator").default;  //生成还原后的代码
const fs = require('fs');

var jscode = fs.readFileSync("./slide_7.7.4.js", {
    encoding: "utf-8"
});
const visitor = {
        StringLiteral(path) {
                delete path.node.extra
            }
}

let ast = parser.parse(jscode);
traverse(ast, visitor);
let {code} = generator(ast, opts = {jsescOption: {"minimal": true}});
fs.writeFile('decode_slide.js', code, (err)=>{});