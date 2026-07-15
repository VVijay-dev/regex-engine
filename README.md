# Regex Engine

A lightweight, custom Regular Expression (Regex) engine built from scratch in Python. Instead of relying on built-in tools, this project implements a complete compilation pipeline—transforming a raw regex pattern into tokens, building a structured Abstract Syntax Tree (AST), and evaluating text inputs via a custom matching engine.

## Core Architecture

The engine processes patterns and matches strings using a classic three-stage compiler workflow:

