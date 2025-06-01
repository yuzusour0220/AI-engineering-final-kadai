"use client";

import { Editor } from "@monaco-editor/react";

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language?: string;
  height?: string;
}

export default function CodeEditor({ 
  value, 
  onChange, 
  language = "python", 
  height = "400px" 
}: CodeEditorProps) {
  const handleEditorChange = (value: string | undefined) => {
    onChange(value || "");
  };

  return (
    <div className="border border-gray-300 rounded-lg overflow-hidden">
      <Editor
        height={height}
        defaultLanguage={language}
        value={value}
        onChange={handleEditorChange}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          insertSpaces: true,
          wordWrap: "on",
        }}
      />
    </div>
  );
}
