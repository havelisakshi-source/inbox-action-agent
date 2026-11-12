import { useState, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { agentService } from '../services/agent';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Send, Bot, User, Sparkles } from 'lucide-react';
import { cn } from '../utils/cn';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export function Assistant() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: "Hi! I'm your AI inbox assistant. Ask me things like 'What are my recent promotions?' or 'Do I have any important emails?'" }
  ]);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const chatMutation = useMutation({
    mutationFn: agentService.chat,
    onSuccess: (data) => {
      setMessages((prev) => [...prev, { role: 'assistant', content: data }]);
    },
    onError: () => {
      setMessages((prev) => [...prev, { role: 'assistant', content: "Sorry, I ran into an error trying to process that." }]);
    }
  });

  const handleSend = () => {
    if (!input.trim() || chatMutation.isPending) return;
    
    const userMessage = input.trim();
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    chatMutation.mutate(userMessage);
  };

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, chatMutation.isPending]);

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-8rem)] flex flex-col space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-brand-500" />
          AI Assistant
        </h1>
        <p className="text-slate-500 text-sm mt-1">Chat with your inbox using natural language.</p>
      </div>

      <Card className="flex-1 flex flex-col overflow-hidden">
        {/* Chat History */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {messages.map((msg, idx) => (
            <div key={idx} className={cn("flex gap-3", msg.role === 'user' ? "flex-row-reverse" : "")}>
              <div className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
                msg.role === 'user' ? "bg-slate-200 dark:bg-slate-700" : "bg-brand-100 dark:bg-brand-900/50 text-brand-600 dark:text-brand-400"
              )}>
                {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
              </div>
              <div className={cn(
                "px-4 py-3 rounded-2xl max-w-[80%] text-sm whitespace-pre-wrap",
                msg.role === 'user' 
                  ? "bg-brand-600 text-white rounded-tr-sm" 
                  : "bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 rounded-tl-sm"
              )}>
                {msg.content}
              </div>
            </div>
          ))}
          
          {chatMutation.isPending && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-brand-100 dark:bg-brand-900/50 flex items-center justify-center flex-shrink-0">
                <Bot className="w-5 h-5 text-brand-600 dark:text-brand-400" />
              </div>
              <div className="px-4 py-3 rounded-2xl bg-slate-100 dark:bg-slate-800 rounded-tl-sm flex items-center gap-2">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-150" />
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-300" />
              </div>
            </div>
          )}
          <div ref={endOfMessagesRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
          <form 
            onSubmit={(e) => { e.preventDefault(); handleSend(); }}
            className="flex gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about your emails..."
              className="flex-1 h-10 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
              disabled={chatMutation.isPending}
            />
            <Button type="submit" disabled={!input.trim() || chatMutation.isPending}>
              <Send className="w-4 h-4" />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  );
}