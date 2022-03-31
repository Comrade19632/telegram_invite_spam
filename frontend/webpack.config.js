const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
    mode: 'development',
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].[hash].js',
    },
    devServer: {
        port: 3010,
        watchContentBase: true,
    },
    module: {
        rules: [
            {
                test: /\.s[ac]ss$/i, 
                use: [
                    // Creates `style` nodes from JS strings
                    'style-loader',
                    // Translates CSS into CommonJS
                    'css-loader',
                    // Compiles Sass to CSS
                    'sass-loader',
                ],
            },
            {
                // look for .js or .jsx files
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    // what to use to compile them 
                    loader: 'babel-loader',
                    options: {
                        cacheDirectory: true,
                        cacheCompression: false,
                    },
                },
            },
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
        // Options similar to the same options in webpackOptions.output
        // both options are optional
            filename: '[name].css',
            chunkFilename: '[id].css',
        }),
    ],
    resolve: {
        extensions: ['.js', '.jsx'],
        alias: {
            '@': path.resolve(__dirname, 'src'),
            styles: path.resolve(__dirname, './src/styles'),
            components: path.resolve(__dirname, './src/components'),
            containers: path.resolve(__dirname, './src/containers'),
            store: path.resolve(__dirname, './src/redux'),

        },
    },
}
