import React from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, Clock, ArrowRight, Scale, BookOpen, HelpCircle, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const HomePage = ({ user, setUser }) => {
    const navigate = useNavigate();

    const handleSignOut = () => {
        localStorage.removeItem('user');
        setUser(null);
        navigate('/');
    };

    const facts = [
        {
            icon: <Scale className="text-legal-gold" size={24} />,
            title: "Judicial Backlog",
            text: "Over 40 million cases are pending in Indian courts, highlighting the need for accessible legal aid."
        },
        {
            icon: <BookOpen className="text-legal-navy" size={24} />,
            title: "Legal Literacy",
            text: "A significant portion of the population is unaware of their fundamental rights and legal remedies."
        }
    ];

    const faqs = [
        {
            q: "What can this chatbot do?",
            a: "It can provide preliminary legal information, explain legal terms, and guide you through basic procedures."
        },
        {
            q: "Is the advice binding?",
            a: "No, this is an AI assistant for informational purposes only. Always consult a qualified lawyer for legal action."
        }
    ];

    const previousChats = [
        { id: 1, title: "Property Dispute Inquiry", date: "2 days ago" },
        { id: 2, title: "Traffic Violation Fine", date: "5 days ago" },
        { id: 3, title: "Rental Agreement Draft", date: "1 week ago" },
    ];

    return (
        <div className="w-full max-w-6xl p-6 h-[85vh] flex flex-col">
            {/* Header */}
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-serif font-bold text-legal-navy">
                        Welcome, <span className="text-legal-gold">{user?.firstName} {user?.lastName}</span>
                    </h1>
                    <p className="text-legal-muted text-sm">Your Legal Aid Dashboard</p>
                </div>
                <button
                    onClick={handleSignOut}
                    className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 border border-red-200 rounded-lg hover:bg-red-100 transition-colors"
                >
                    <LogOut size={18} /> Sign Out
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 flex-1 overflow-hidden">
                {/* Left Section: Facts & FAQs */}
                <motion.div
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="space-y-6 overflow-y-auto pr-2 custom-scrollbar"
                >
                    <section>
                        <h2 className="text-2xl font-serif font-bold text-legal-navy mb-4 flex items-center gap-2">
                            <Scale /> Legal Insights
                        </h2>
                        <div className="grid gap-4">
                            {facts.map((fact, index) => (
                                <div key={index} className="bg-white border border-legal-border p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                                    <div className="flex items-start gap-3">
                                        <div className="p-2 bg-legal-bg rounded-lg">{fact.icon}</div>
                                        <div>
                                            <h3 className="font-bold text-legal-text mb-1">{fact.title}</h3>
                                            <p className="text-legal-muted text-sm">{fact.text}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    <section>
                        <h2 className="text-2xl font-serif font-bold text-legal-navy mb-4 flex items-center gap-2">
                            <HelpCircle /> FAQ
                        </h2>
                        <div className="space-y-3">
                            {faqs.map((faq, index) => (
                                <div key={index} className="bg-white border border-legal-border p-4 rounded-xl shadow-sm">
                                    <h3 className="font-bold text-legal-navy mb-1 text-sm">{faq.q}</h3>
                                    <p className="text-legal-muted text-sm">{faq.a}</p>
                                </div>
                            ))}
                        </div>
                    </section>
                </motion.div>

                {/* Right Section: Actions */}
                <motion.div
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex flex-col gap-6 h-full"
                >
                    {/* Start Chat - Top Half */}
                    <div className="flex-1 bg-gradient-to-br from-legal-navy to-blue-900 rounded-2xl p-8 flex flex-col items-center justify-center text-center shadow-xl relative overflow-hidden group">
                        <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                        <div className="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <MessageSquare size={40} className="text-white" />
                        </div>

                        <h2 className="text-3xl font-serif font-bold text-white mb-2">Start New Session</h2>
                        <p className="text-blue-100 mb-8 max-w-xs">Begin a new consultation with the AI Legal Assistant.</p>

                        <button
                            onClick={() => navigate('/chat')}
                            className="px-8 py-4 bg-white text-legal-navy font-bold rounded-xl flex items-center gap-2 hover:bg-blue-50 transition-all transform hover:-translate-y-1 shadow-lg"
                        >
                            Initialize Chat <ArrowRight size={20} />
                        </button>
                    </div>

                    {/* Previous Chats - Bottom Half */}
                    <div className="flex-1 bg-white border border-legal-border rounded-2xl p-6 shadow-sm flex flex-col">
                        <h3 className="text-xl font-serif font-bold text-legal-navy mb-4 flex items-center gap-2">
                            <Clock size={20} /> Previous Sessions
                        </h3>

                        <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar">
                            {previousChats.map((chat) => (
                                <div key={chat.id} className="p-3 bg-legal-bg rounded-lg border border-legal-border hover:border-legal-navy/30 transition-all cursor-pointer group">
                                    <div className="flex justify-between items-center">
                                        <span className="font-medium text-legal-text group-hover:text-legal-navy transition-colors">{chat.title}</span>
                                        <span className="text-xs text-legal-muted">{chat.date}</span>
                                    </div>
                                </div>
                            ))}
                            {/* Dummy filler to show scroll if needed */}
                            <div className="p-3 bg-legal-bg rounded-lg border border-legal-border opacity-50">
                                <span className="text-legal-muted text-sm italic">End of history</span>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default HomePage;
