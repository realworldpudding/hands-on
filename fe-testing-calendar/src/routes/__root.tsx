import { createRouter, createRootRoute, Link, Outlet } from '@tanstack/react-router'
import {  } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'
import { z } from 'zod'

import {
  createRoute,
} from '@tanstack/react-router'
import Calendar from '../pages/calendar/Calendar'

const RootRoute = createRootRoute({
  component: () => {
    return (
      <>
        <Outlet />
        <TanStackRouterDevtools />
      </>
    )
  },
})

export const calendarRoute = createRoute({
  getParentRoute: () => RootRoute,
  path: '/calendar/$slug',
  component: Calendar,
  params: z.object({
    slug: z.string().min(4),
  }),
  validateSearch: z.object({
    year: z.number().min(2024).optional().default(() => new Date().getFullYear()),
    month: z.number().min(1).max(12).optional().default(() => new Date().getMonth() + 1),
  }),
})


export const routeTree = RootRoute.addChildren([calendarRoute])

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}