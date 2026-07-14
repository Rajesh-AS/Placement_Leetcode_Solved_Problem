import { useState, useEffect, useRef } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { Send, User as UserIcon } from 'lucide-react';

export function ChatPage() {
  const { user } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [activeConv, setActiveConv] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Fetch conversations
    api.get('/chat/conversations/')
      .then(res => {
        setConversations(res.data);
        if (res.data.length > 0) {
          setActiveConv(res.data[0]);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch conversations', err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (activeConv) {
      // Fetch messages for active conversation
      api.get(`/chat/conversations/${activeConv.id}/messages/`)
        .then(res => {
          setMessages(res.data.reverse()); // Assuming backend returns descending order
          scrollToBottom();
        });

      // Setup WebSocket connection
      // Note: In production, use wss:// and handle auth token in query params if needed
      const wsUrl = `ws://localhost:8000/ws/chat/${activeConv.id}/`;
      ws.current = new WebSocket(wsUrl);

      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setMessages(prev => [...prev, data]);
        scrollToBottom();
      };

      return () => {
        if (ws.current) ws.current.close();
      };
    }
  }, [activeConv]);

  const scrollToBottom = () => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !ws.current || ws.current.readyState !== WebSocket.OPEN) return;

    ws.current.send(JSON.stringify({
      message: newMessage,
      sender_id: user.id
    }));
    
    setNewMessage('');
  };

  if (loading) return <div className="p-8 text-center">Loading messages...</div>;

  return (
    <div className="max-w-7xl mx-auto h-[calc(100vh-4rem)] flex overflow-hidden bg-background">
      {/* Sidebar - Conversations List */}
      <div className="w-1/3 border-r flex flex-col bg-card">
        <div className="p-4 border-b">
          <h2 className="text-xl font-bold">Messages</h2>
        </div>
        <div className="overflow-y-auto flex-1">
          {conversations.length === 0 ? (
            <div className="p-8 text-center text-muted-foreground">No conversations yet</div>
          ) : (
            conversations.map(conv => {
              const otherUser = conv.participants.find(p => p.id !== user.id);
              const isActive = activeConv?.id === conv.id;
              return (
                <div 
                  key={conv.id} 
                  onClick={() => setActiveConv(conv)}
                  className={`p-4 border-b cursor-pointer hover:bg-accent transition-colors flex items-center gap-3 ${isActive ? 'bg-accent' : ''}`}
                >
                  <div className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center shrink-0 overflow-hidden">
                    {otherUser?.profile_picture ? (
                      <img src={otherUser.profile_picture} alt="Avatar" className="w-full h-full object-cover" />
                    ) : (
                      <UserIcon className="h-5 w-5 text-muted-foreground" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium truncate">{otherUser?.first_name} {otherUser?.last_name}</h3>
                    {conv.last_message && (
                      <p className="text-sm text-muted-foreground truncate">{conv.last_message.content}</p>
                    )}
                  </div>
                </div>
              )
            })
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-background">
        {activeConv ? (
          <>
            {/* Chat Header */}
            <div className="p-4 border-b bg-card flex items-center gap-3 shadow-sm z-10">
              <div className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center shrink-0">
                 <UserIcon className="h-5 w-5 text-muted-foreground" />
              </div>
              <div>
                <h3 className="font-bold">
                  {activeConv.participants.find(p => p.id !== user.id)?.first_name}
                </h3>
              </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, idx) => {
                const isMe = msg.sender === user.id || msg.sender_id === user.id;
                return (
                  <div key={idx} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[70%] rounded-2xl px-4 py-2 ${
                      isMe ? 'bg-primary text-primary-foreground rounded-br-none' : 'bg-muted text-foreground rounded-bl-none'
                    }`}>
                      <p>{msg.content || msg.message}</p>
                    </div>
                  </div>
                )
              })}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-card border-t">
              <form onSubmit={handleSendMessage} className="flex gap-2">
                <Input 
                  value={newMessage} 
                  onChange={e => setNewMessage(e.target.value)}
                  placeholder="Type a message..."
                  className="flex-1"
                />
                <Button type="submit" size="icon"><Send className="h-4 w-4" /></Button>
              </form>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            Select a conversation to start chatting
          </div>
        )}
      </div>
    </div>
  );
}
