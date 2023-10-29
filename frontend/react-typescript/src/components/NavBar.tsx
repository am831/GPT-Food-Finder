export function NavBar() {
  return (
    <div className='navbar bg-base-100'>
      <div className='flex-1'>
        <a className='btn btn-ghost normal-case text-xl'>Restaurant App</a>
      </div>
      <div className='flex-none'>
        <button
          className='btn btn-square btn-ghost'
          onClick={() => {
            const modal = document.getElementById(
              'my_modal_3'
            ) as HTMLDialogElement
            if (modal) {
              modal.showModal()
            }
          }}
        >
          <dialog id='my_modal_3' className='modal'>
            <div className='modal-box'>
              <form method='dialog'>
                <button className='btn btn-sm btn-circle btn-ghost absolute right-2 top-2'>
                  ✕
                </button>
              </form>
              <div className='grid grid-cols-1 gap-3'>
                <h3 className='font-bold text-lg'>Settings</h3>
                <select className='select select-primary w-full max-w-xs'>
                  <option disabled selected>
                    Change the default radius
                  </option>
                  <option value={1}>1 mile</option>
                  <option value={2}>2 miles</option>
                  <option value={5}>5 miles</option>
                  <option value={10}>10 miles</option>
                </select>
              </div>
            </div>
          </dialog>

          <svg
            xmlns='http://www.w3.org/2000/svg'
            fill='none'
            viewBox='0 0 24 24'
            className='inline-block w-5 h-5 stroke-current'
          >
            <path
              strokeLinecap='round'
              strokeLinejoin='round'
              strokeWidth='2'
              d='M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z'
            ></path>
          </svg>
        </button>
      </div>
    </div>
  )
}
