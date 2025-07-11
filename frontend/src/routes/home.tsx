import { LoginForm } from "@/components/login-form";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/home")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div className="text-lg font-bold bg-amber-700 p-4 text-center text-white">
      <span>TESTTTTTTTT</span>
      <LoginForm />
    </div>
  );
}
