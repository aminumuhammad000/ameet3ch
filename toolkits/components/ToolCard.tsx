import React from 'react';
import Link from 'next/link';
import {
  FileText,
  Receipt,
  Calculator,
  MessageSquare,
  Sparkles,
  Lightbulb,
  FileSpreadsheet,
  ArrowRight,
  LucideIcon,
} from 'lucide-react';
import { ToolItem } from '@/lib/tools-data';

const iconMap: Record<string, LucideIcon> = {
  FileText,
  Receipt,
  Calculator,
  MessageSquare,
  Sparkles,
  Lightbulb,
  FileSpreadsheet,
};

interface ToolCardProps {
  tool: ToolItem;
}

export default function ToolCard({ tool }: ToolCardProps) {
  const Icon = iconMap[tool.icon] || FileText;

  return (
    <div className="group relative flex flex-col justify-between bg-white rounded-2xl p-6 border border-slate-200/80 hover:border-purple-300 shadow-sm hover:shadow-xl transition-all duration-300">
      <div>
        <div className="flex items-center justify-between gap-3 mb-4">
          <div className="w-12 h-12 rounded-xl bg-purple-50 group-hover:bg-purple-100 flex items-center justify-center text-purple-700 transition">
            <Icon className="w-6 h-6" />
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-semibold tracking-wide uppercase px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
              Free
            </span>
            <span className="text-[11px] font-medium text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md">
              {tool.category}
            </span>
          </div>
        </div>

        <h3 className="text-lg font-bold text-slate-900 group-hover:text-purple-700 transition mb-2">
          {tool.name}
        </h3>
        <p className="text-sm text-slate-600 leading-relaxed line-clamp-3 mb-6">
          {tool.description}
        </p>
      </div>

      <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
        <Link
          href={tool.slug}
          className="inline-flex items-center gap-2 text-sm font-semibold text-purple-700 group-hover:text-purple-850 transition"
        >
          <span>Use Free Tool</span>
          <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition" />
        </Link>
        <span className="text-xs text-slate-600">No signup</span>
      </div>
    </div>
  );
}
