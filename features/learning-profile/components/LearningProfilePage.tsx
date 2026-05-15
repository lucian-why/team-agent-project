'use client'

import Link from 'next/link'
import { useMemo } from 'react'
import { useRouter } from 'next/navigation'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import { AppShell } from '@/components/layout/AppShell'
import { GuestFeaturePlaceholder } from '@/components/common/GuestFeaturePlaceholder'
import { useAuthStore } from '@/lib/stores/auth-store'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { AlertCircle, BookOpenCheck, FileQuestion, RotateCw, Brain } from 'lucide-react'
import { useNotebooks } from '@/lib/hooks/use-notebooks'
import { cn } from '@/lib/utils'
import { ProfileMetric, WrongQuestionItem } from './LearningProfileCard'
import type { WrongQuestionGroup } from './learning-profile-types'
import { buildWrongQuestionGroups } from './learning-profile-utils'

/**
 * 学习画像页面组件
 *
 * 展示学生的错题集，按 AI 笔记本分组。
 */
export default function LearningProfilePage() {
  const isGuest = useAuthStore((s) => s.isGuest)
  const router = useRouter()

  if (isGuest) {
    return (
      <AppShell>
        <GuestFeaturePlaceholder
          icon={Brain}
          title="错题集"
          description="错题复盘功能需要登录后使用。"
          onLoginClick={() => router.push('/login')}
        />
      </AppShell>
    )
  }
  const { data: notebooks, isLoading } = useNotebooks(false)
  const groups = useMemo(() => buildWrongQuestionGroups(notebooks ?? []), [notebooks])
  const wrongQuestionCount = groups.reduce(
    (sum, group) => sum + group.wrongQuestions.length,
    0
  )
  const notebooksWithMistakes = groups.filter((group) => group.wrongQuestions.length > 0).length

  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="space-y-6 p-6">
          <section className="rounded-2xl border border-border/50 bg-card/80 p-6 backdrop-blur-sm" aria-label="学习画像错题集">
            <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-rose-500 to-pink-500 text-white">
                    <BookOpenCheck className="h-4 w-4" />
                  </div>
                  <span>学习画像</span>
                </div>
                <h1 className="mt-3 text-headline">错题集</h1>
                <p className="mt-1 text-sm text-muted-foreground">
                  按AI笔记本汇总测验错题、错误模式和下一步练习入口。
                </p>
              </div>

              <div className="grid min-w-0 gap-3 sm:grid-cols-3 lg:w-[520px]">
                <ProfileMetric label="AI笔记本" value={`${groups.length}`} hint="按课程分组" color="blue" />
                <ProfileMetric label="错题" value={`${wrongQuestionCount}`} hint="来自测验批改" color="rose" />
                <ProfileMetric label="待复盘" value={`${notebooksWithMistakes}`} hint="有错题的AI笔记本" color="amber" />
              </div>
            </div>

            {isLoading ? (
              <div className="mt-5 flex items-center gap-2 rounded-lg bg-background px-4 py-4 text-sm text-muted-foreground">
                <RotateCw className="h-4 w-4 animate-spin" />
                正在同步错题集...
              </div>
            ) : groups.length === 0 ? (
              <div className="mt-5 rounded-lg bg-background px-4 py-5">
                <p className="text-sm font-medium">暂无AI笔记本</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  创建AI笔记本并添加资料后，可以从工作室生成测验题。
                </p>
              </div>
            ) : (
              <Accordion type="multiple" className="mt-5 rounded-2xl border border-border/50 bg-background/80 px-4 backdrop-blur-sm">
                {groups.map((group) => (
                  <AccordionItem key={group.notebookId} value={group.notebookId} className="border-b border-border/40 last:border-b-0">
                    <AccordionTrigger className="hover:no-underline py-4">
                      <div className="flex min-w-0 flex-1 flex-wrap items-center gap-3 text-left">
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
                    </AccordionTrigger>
                    <AccordionContent>
                      {group.wrongQuestions.length > 0 ? (
                        <div className="space-y-3 pb-2">
                          {group.wrongQuestions.map((question, index) => (
                            <WrongQuestionItem
                              key={question.id}
                              question={question}
                              index={index}
                            />
                          ))}
                        </div>
                      ) : (
                        <div className="flex flex-col gap-3 rounded-xl border border-dashed border-border/60 bg-muted/20 p-4 sm:flex-row sm:items-center sm:justify-between">
                          <div>
                            <p className="text-sm font-medium">这个AI笔记本还没有收集错题</p>
                            <p className="mt-1 text-sm text-muted-foreground">
                              进入AI笔记本后从工作室生成测验，作答后会沉淀错题。
                            </p>
                          </div>
                          <Button asChild size="sm" className="shrink-0">
                            <Link href={group.quizHref}>
                              <FileQuestion className="h-4 w-4" />
                              生成测验
                            </Link>
                          </Button>
                        </div>
                      )}
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            )}
          </section>
        </div>
      </div>
    </AppShell>
  )
}
