import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { X, Send, Bot, Settings, Key } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface OpenAIChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const OpenAIChat = ({ isOpen, onClose }: OpenAIChatProps) => {
  const [apiKey, setApiKey] = useState(() => localStorage.getItem("openai_api_key") || "");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showApiKeyInput, setShowApiKeyInput] = useState(false);
  const { toast } = useToast();

  const sendMessage = async () => {
    // If server has key, local key is optional; we still allow local override.

    if (!message.trim()) return;

    const userMessage = message.trim();
    setMessage("");
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const apiBase = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';
      // Prefer calling our backend so API key can be stored server-side via .env
      const response = await fetch(`${apiBase}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(apiKey.trim() ? { 'X-OpenAI-Api-Key': apiKey.trim() } : {}),
        },
        body: JSON.stringify({
          model: 'gpt-4o-mini',
          messages: [
            { role: 'system', content: 'Context: ResumeAI web app user asking for career/resume help.' },
            ...messages,
            { role: 'user', content: userMessage }
          ]
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from OpenAI');
      }

      const data = await response.json();
      const assistantMessage = data.choices[0]?.message?.content || 'Sorry, I could not generate a response.';
      
      setMessages(prev => [...prev, { role: 'assistant', content: assistantMessage }]);
    } catch (error) {
      console.error('OpenAI API Error:', error);
      toast({
        title: "Error",
        description: "Failed to get response from OpenAI. Please check your API key and try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-end p-6">
      <Card className="glass-card w-96 h-[500px] flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-gradient-from to-gradient-via rounded-lg flex items-center justify-center">
              <Bot className="h-4 w-4 text-white" />
            </div>
            <span className="font-semibold">AI Assistant</span>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setShowApiKeyInput(!showApiKeyInput)}
              className="p-2 hover:bg-secondary/20"
            >
              <Settings className="h-4 w-4" />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={onClose}
              className="p-2 hover:bg-secondary/20"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {showApiKeyInput && (
          <div className="p-4 border-b border-border/20 bg-muted/20">
            <div className="flex items-center space-x-2 mb-2">
              <Key className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">OpenAI API Key</span>
            </div>
            <Input
              type="password"
              placeholder="sk-..."
              value={apiKey}
              onChange={(e) => {
                setApiKey(e.target.value);
                localStorage.setItem("openai_api_key", e.target.value);
              }}
              className="glass border-border/30"
            />
            <p className="text-xs text-muted-foreground mt-1">
              Your API key is stored locally and not sent to our servers.
            </p>
          </div>
        )}

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-muted-foreground py-8">
              <Bot className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p className="text-sm">Hi, how can I help you?</p>
              <p className="text-xs mt-2">Ask me for career advice, resume tips, or role suggestions.</p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-2xl ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-r from-gradient-from to-gradient-via text-white'
                      : 'glass border border-border/30'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="glass border border-border/30 p-3 rounded-2xl">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-primary rounded-full animate-pulse delay-75"></div>
                  <div className="w-2 h-2 bg-primary rounded-full animate-pulse delay-150"></div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="p-4 border-t border-border/20">
          <div className="flex space-x-2">
            <Textarea
              placeholder="Ask me anything about your career..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              className="glass border-border/30 resize-none"
              rows={1}
            />
            <Button
              onClick={sendMessage}
              disabled={isLoading || !message.trim()}
              className="bg-gradient-to-r from-gradient-from to-gradient-via text-white shadow-glow hover:pulse-glow transition-all duration-300"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default OpenAIChat;