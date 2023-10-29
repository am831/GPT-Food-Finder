function HeadHero() {
  return (
    <div className="hero min-h-screen">
      <div className="hero-content flex-col lg:flex-row-reverse">
        <div className="flex flex-col place-items-center">
          <h1 className="text-5xl font-bold">The Restaurant App</h1>
          <p className="py-6">
            A chat app designed to match you with a personalized AI in order to save you time and money.
          </p>
        </div>
      </div>
    </div>
  )
}
export function HomePage() {
  return (
      <HeadHero></HeadHero>
  )
}
