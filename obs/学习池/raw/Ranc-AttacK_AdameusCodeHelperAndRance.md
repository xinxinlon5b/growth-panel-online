# Ranc-AttacK/AdameusCodeHelperAndRance

- **Stars**: 2
- **描述**: AI Code Helper 是一个基于Spring Boot 3和LangChain4j构建的企业级 AI编程助手后端服务。本项目旨在探索 Java 生态下的 LLM 应用开发最佳实践，集成了 RAG (检索增强生成)、分布式会话管理、多模态交互以及前沿的 MCP (Model Context Protocol)协议。
- **链接**: https://github.com/Ranc-AttacK/AdameusCodeHelperAndRance

```
# 🚀 AI Code Helper (Based on LangChain4j)

[![Java](https://img.shields.io/badge/Java-17%2B-orange)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-green)](https://spring.io/projects/spring-boot)
[![LangChain4j](https://img.shields.io/badge/LangChain4j-0.3x-blue)](https://github.com/langchain4j/langchain4j)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

> **"Every theory is a possibility to be tested."** — *Amadeus System*

## 📖 简介 (Introduction)

**AI Code Helper** 是一个基于 **Spring Boot 3** 和 **LangChain4j** 构建的企业级 AI 编程助手后端服务。
本项目旨在探索 Java 生态下的 LLM 应用开发最佳实践，集成了 **RAG (检索增强生成)**、**分布式会话管理**、**多模态交互** 以及前沿的 **MCP (Model Context Protocol)** 协议。

它不仅是一个简单的聊天机器人，更是一个具备**记忆**、**知识库**和**工具调用能力**的智能 Agent 框架。

## ✨ 核心特性 (Key Features)

*   **🧠 声明式 AI 服务**：基于 LangChain4j 的 `AiServices` 声明式接口，屏蔽底层 LLM 调用细节。
*   **💾 分布式记忆 (Distributed Memory)**：利用 **Redis** 实现会话持久化，支持滑动窗口 (Window Memory) 策略，完美适配微服务架构。
*   **📚 RAG 知识库**：集成向量检索流水线 (Embedding Store + Content Retriever)，支持私有文档问答，减少 AI 幻觉。
*   **⚡ 响应式流式输出**：基于 **Spring WebFlux (Project Reactor)** 实现 SSE (Server-Sent Events) 流式响应，提供极致的用户交互体验。
*   **🛠️ MCP 协议集成**：(Experimental) 支持 **Model Context Protocol**，实现了 Java 后端与 Python 工具脚本 (如 `markitdown`) 的跨进程协同。
*   **🛡️ 安全围栏**：内置 `InputGuardrails`，有效拦截 Prompt Injection 及敏感违规内容。
*   **🔧 本地工具调用**：支持 `@Tool` 注解定义的 Function Calling，赋予 AI 操作本地文件系统的能力。

## 🛠️ 技术栈 (Tech Stack)

*   **Language**: Java 17+
*   **Framework**: Spring Bo
```
