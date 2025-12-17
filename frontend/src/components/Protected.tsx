"use client"

import React from "react"
import { useRouter } from "next/navigation"
import { isAuthenticated } from "@/lib/auth"

export default function Protected({ children }: { children: React.ReactNode }) {
    const router = useRouter()

    React.useEffect(() => {
        if (!isAuthenticated()) {
            router.push('/login')
        }
    }, [])

    return <>{children}</>
}
