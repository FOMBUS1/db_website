'use strict'

const path = require('path')
const autoprefixer = require('autoprefixer')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  mode: 'development',
  entry: './src/js/main.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  devServer: {
    static: path.resolve(__dirname, 'dist'),
    host: '0.0.0.0',
    port: 8080,
    open: true,
    hot: true, 
    client: {
      overlay: false,
      webSocketURL: {
        hostname: 'react-tunnel.ngrok.io',
        port: 0,
        protocol: 'wss',
      },
    },
    allowedHosts: 'all',
  },
  plugins: [
    new HtmlWebpackPlugin({ template: './src/html/user.html' }),
    new CopyPlugin({
      patterns: [
          { from: 'src/html/main.html', to: 'main.html' },
          { from: 'src/html/performers.html', to: 'performers.html'},
          { from: 'src/html/albums.html', to: 'albums.html'},
          { from: 'src/html/tracks.html', to: 'tracks.html'},
          { from: 'src/html/playlistChoice.html', to: 'playlistChoice.html'},
          { from: 'src/html/playlist.html', to: 'playlist.html'}
      ]
  })
  ],
  stats: {warnings:false},
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          {
            // Adds CSS to the DOM by injecting a `<style>` tag
            loader: 'style-loader'
          },
          {
            // Interprets `@import` and `url()` like `import/require()` and will resolve them
            loader: 'css-loader'
          },
          {
            // Loader for webpack to process CSS with PostCSS
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  autoprefixer
                ]
              }
            }
          },
          {
            // Loads a SASS/SCSS file and compiles it to CSS
            loader: 'sass-loader'
          }
        ]
      }
    ]
  }
}