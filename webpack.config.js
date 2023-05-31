// Generated using webpack-cli https://github.com/webpack/webpack-cli

const path = require('path');
const fs = require('fs');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const isProduction = process.env.NODE_ENV === 'production';


const stylesHandler = MiniCssExtractPlugin.loader;
const serverRoot = path.resolve(__dirname, "server");


const getDirectories = source => fs.readdirSync(source, {withFileTypes: true})
        .filter(dirent => dirent.isDirectory())
        .map(dirent => dirent.name);
const getFiles = source => fs.readdirSync(source, {withFileTypes: true})
        .filter(dirent => dirent.isFile())
        .map(dirent => dirent.name);


function inputFinder(){
    let appDirs = getDirectories(serverRoot);
    let entry = {};
    for (const appDir of appDirs) {
        const tsSourceDir = path.resolve(serverRoot, appDir, "frontend");
        if(!fs.existsSync(tsSourceDir) || !fs.statSync(tsSourceDir).isDirectory()) continue;

        const entryPoints = getFiles(tsSourceDir);
        for(const entryPoint of entryPoints){
            if(entryPoint.endsWith(".d.ts")) continue;
            const name = path.join(appDir, "static", appDir, entryPoint.slice(0, -3));
            entry[name] = path.join(tsSourceDir, entryPoint);
        }
    }
    return entry;
}




const config = {
    entry: inputFinder(),
    output: {
        path: serverRoot,
        filename: '[name].js'
    },
    devServer: {
        open: true,
        host: 'localhost',
    },
    plugins: [
        // Add your plugins here
        // Learn more about plugins from https://webpack.js.org/configuration/plugins/
    ],
    module: {
        rules: [
            {
                test: /\.(ts|tsx)$/i,
                loader: 'ts-loader',
                exclude: ['/node_modules/'],
            },
            {
                test: /\.css$/i,
                use: [stylesHandler,'css-loader'],
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2|png|jpg|gif)$/i,
                type: 'asset',
            },
            {
                test: /\.html$/i,
                loader: "html-loader",
                options: {
                    esModule: true,
                },
                exclude: ["/node_modules/"]
            },

            // Add your rules for custom modules here
            // Learn more about loaders from https://webpack.js.org/loaders/
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.jsx', '.js', '...', '.html'],
    },
};

module.exports = () => {
    if (isProduction) {
        config.mode = 'production';
    } else {
        config.mode = 'development';
    }
    return config;
};
