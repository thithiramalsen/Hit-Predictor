import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { XCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/solid';

export function Notification({ message, onClose }) {
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        onClose();
      }, 5000); // Auto-dismiss after 5 seconds

      return () => clearTimeout(timer);
    }
  }, [message, onClose]);

  return (
    <AnimatePresence>
      {message && (
        <motion.div
          initial={{ opacity: 0, y: -50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -50, scale: 0.9 }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          className="fixed top-5 left-1/2 -translate-x-1/2 z-50 w-full max-w-md p-4"
        >
          <div className="bg-red-500/90 backdrop-blur-sm text-white p-4 rounded-lg shadow-lg flex items-start space-x-3 border border-red-400">
            <ExclamationTriangleIcon className="h-6 w-6 flex-shrink-0 text-white" />
            <p className="flex-grow text-sm font-semibold">{message}</p>
            <button onClick={onClose} className="p-1 -m-1 rounded-full hover:bg-white/20 transition-colors">
              <XCircleIcon className="h-5 w-5" />
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}