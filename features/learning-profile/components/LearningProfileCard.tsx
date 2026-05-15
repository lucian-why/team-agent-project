'use client'

import { Brain, BookOpenCheck, FileQuestion, RotateCw, AlertCircle } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import type { WrongQuestion, WrongQuestionGroup } from './learning-profile-types'

/**
 * 学习画像指标卡片组件
 */
export function ProfileMetric({
  label,
  value,
  hint,
  color = 'blue',
}: {
  label: string
  value: string
  hint: string
  color?: 'blue' | 'rose' | 'amber' | 'emerald' | 'purple'
}) {
  const colorMap = {
    blue: 'from-purple-500 to-violet-500',
    rose: 'from-rose-500 to-pink-500',
    amber: 'from-amber-500 to-orange-500',
    emerald: 'from-emerald-500 to-teal-500',
    purple: 'from-purple-500 to-violet-500',
  }

  return (
    <div className="rounded-xl border border-border/40 bg-background/80 px-5 py-4 transition-all duration-200 hover:border-primary/20 hover:shadow-card">
      <p className="text-xs font-medium text-muted-foreground">{label}</p>
      <p className={cn('mt-1 text-3xl font-bold tabular-nums bg-gradient-to-r bg-clip-text text-transparent', colorMap[color])}>
        {value}
      </p>
      <p className="mt-1 text-[11px] text-muted-foreground/70">{hint}</p>
    </div>
  )
}

/**
 * 错题项组件
 */
export function WrongQuestionItem({
  question,
  index,
}: {
  question: WrongQuestion
  index: number
}) {
  return (
    <div className="rounded-xl border border-border/50 bg-background p-4 transition-all duration-200 hover:border-rose-200/50 hover:shadow-sm dark:hover:border-rose-900/30">
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="outline" className="text-xs">错题 {index + 1}</Badge>
        <Badge variant="secondary" className="bg-amber-500/10 text-amber-600 border-amber-200/50 text-xs dark:bg-amber-950/30 dark:text-amber-300 dark:border-amber-800/40">
          {question.mistakeType}
        </Badge>
        <span className="text-xs text-muted-foreground">来源：{question.sourceLabel}</span>
      </div>
      <p className="mt-3 text-sm font-medium leading-relaxed">{question.question}</p>
      <div className="mt-3 grid gap-2 md:grid-cols-2">
        <div className="rounded-lg border-l-4 border-rose-400 bg-rose-50/80 px-3 py-2.5 text-sm text-rose-700 dark:bg-rose-950/20 dark:text-rose-300">
          <span className="text-[11px] font-medium text-rose-500/80 uppercase tracking-wider">我的答案</span>
          <div className="mt-0.5 font-medium">{question.userAnswer}</div>
        </div>
        <div className="rounded-lg border-l-4 border-emerald-400 bg-emerald-50/80 px-3 py-2.5 text-sm text-emerald-700 dark:bg-emerald-950/20 dark:text-emerald-300">
          <span className="text-[11px] font-medium text-emerald-500/80 uppercase tracking-wider">正确答案</span>
          <div className="mt-0.5 font-medium">{question.correctAnswer}</div>
        </div>
      </div>
      <div className="mt-3 flex items-center gap-2 rounded-lg bg-muted/30 px-3 py-2 text-xs text-muted-foreground">
        <AlertCircle className="h-3.5 w-3.5 shrink-0 text-amber-500" />
        建议：先复盘来源片段，再生成同类变式题。
      </div>
    </div>
  )
}

/**
 * 错题分组组件
 */
export function WrongQuestionGroupCard({ group }: { group: WrongQuestionGroup }) {
  return (
    <div className="rounded-xl border border-border/50 bg-background/80 p-4 backdrop-blur-sm">
      <div className="flex min-w-0 flex-1 flex-wrap items-center gap-3">
        <span className="min-w-0 truncate text-sm font-semibold">
          {group.notebookName}
        </span>
        {group.wrongQuestions.length > 0 ? (
          <Badge variant="secondary" className="bg-rose-500/10 text-rose-600 border-rose-200/50 dark:bg-rose-950/30 dark:text-rose-300 dark:border-rose-800/40">
            {group.wrongQuestions.length} 条错题
          </Badge>
        ) : (
          <Badge variant="outline" className="text-muted-foreground/70">暂无错题</Badge>
        )}
        {group.frequentMistakes.length > 0 && (
          <span className="truncate text-xs text-muted-foreground">
            高频错误：{group.frequentMistakes.join('、')}
          </span>
        )}
      </div>
      {group.wrongQuestions.length > 0 ? (
        <div className="mt-3 space-y-3">
          {group.wrongQuestions.map((question, index) => (
            <WrongQuestionItem
              key={question.id}
              question={question}
              index={index}
            />
          ))}
        </div>
      ) : (
        <div className="mt-3 flex flex-col gap-3 rounded-xl border border-dashed border-border/60 bg-muted/20 p-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-medium">这个AI笔记本还没有收集错题</p>
            <p className="mt-1 text-sm text-muted-foreground">
              进入AI笔记本后从工作室生成测验，作答后会沉淀错题。
            </p>
          </div>
          <Button asChild size="sm" className="shrink-0">
            <a href={group.quizHref}>
              <FileQuestion className="h-4 w-4" />
              生成测验
            </a>
          </Button>
        </div>
      )}
    </div>
  )
}
