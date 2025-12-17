"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { ThemeToggle } from "@/components/theme-toggle"
import { analyzeText } from "@/lib/api"
import { Loader2, Sparkles } from "lucide-react"

export default function Home() {
  const [name, setName] = useState("")
  const [businessType, setBusinessType] = useState("")
  const [text, setText] = useState("")
  const [analysis, setAnalysis] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!text.trim()) {
      setError("Please enter some text to analyze")
      return
    }

    setLoading(true)
    setError("")
    setAnalysis("")

    try {
      const result = await analyzeText({
        name: name || undefined,
        business_type: businessType || undefined,
        text: text.trim(),
      })
      setAnalysis(result.analysis)
    } catch (err) {
      setError("Failed to analyze text. Please ensure the backend is running.")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center">
              <Sparkles className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                VidioAgent
              </h1>
              <p className="text-sm text-muted-foreground">AI Customer Relations</p>
            </div>
          </div>
          <ThemeToggle />
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Input Form */}
          <Card className="shadow-xl border-purple-100 dark:border-purple-900">
            <CardHeader>
              <CardTitle className="text-2xl">Get AI Analysis</CardTitle>
              <CardDescription>
                Enter your details and text for personalized AI insights
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <label htmlFor="name" className="text-sm font-medium">
                    Name (Optional)
                  </label>
                  <Input
                    id="name"
                    placeholder="Your name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="businessType" className="text-sm font-medium">
                    Business Type (Optional)
                  </label>
                  <Input
                    id="businessType"
                    placeholder="e.g., Bakery, Salon, Tech Startup"
                    value={businessType}
                    onChange={(e) => setBusinessType(e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="text" className="text-sm font-medium">
                    Your Message <span className="text-destructive">*</span>
                  </label>
                  <Textarea
                    id="text"
                    placeholder="How can I get more customers for my business?"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    rows={6}
                    className="resize-none"
                  />
                </div>

                {error && (
                  <div className="p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
                    {error}
                  </div>
                )}

                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                  size="lg"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Sparkles className="mr-2 h-4 w-4" />
                      Analyze with AI
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Analysis Result */}
          <Card className="shadow-xl border-blue-100 dark:border-blue-900">
            <CardHeader>
              <CardTitle className="text-2xl">AI Analysis</CardTitle>
              <CardDescription>
                Your personalized insights powered by Llama 3
              </CardDescription>
            </CardHeader>
            <CardContent>
              {analysis ? (
                <div className="prose dark:prose-invert max-w-none">
                  <div className="p-4 rounded-lg bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-950/20 dark:to-blue-950/20 border border-purple-200 dark:border-purple-800">
                    <p className="whitespace-pre-wrap text-sm leading-relaxed">
                      {analysis}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-64 text-center text-muted-foreground">
                  <Sparkles className="w-16 h-16 mb-4 opacity-20" />
                  <p className="text-lg font-medium">No analysis yet</p>
                  <p className="text-sm mt-2">
                    Enter your message and click "Analyze with AI" to get started
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-sm text-muted-foreground">
          <p>Powered by Llama 3 via Groq • Built with Next.js & FastAPI</p>
        </div>
      </div>
    </div>
  )
}
