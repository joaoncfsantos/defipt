import { useDynamicContext } from "@dynamic-labs/sdk-react-core";
import { useTokenBalances } from "@dynamic-labs/sdk-react-core";
import { useEffect, useState } from "react";

export function UserInfo() {
  const { primaryWallet } = useDynamicContext();
  const { tokenBalances, isLoading, isError, error } = useTokenBalances();

  // Force re-render when tokenBalances changes
  useEffect(() => {
    if (tokenBalances) {
      console.log("Token balances updated:", tokenBalances);
    }
  }, [tokenBalances]);

  if (!primaryWallet) {
    return (
      <div className="mt-4">
        <p className="text-neutral-800">
          Please connect your wallet to view balances
        </p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="mt-4">
        <p className="text-neutral-800">Loading token balances...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="mt-4">
        <p className="text-red-500">Error loading token balances: {error}</p>
      </div>
    );
  }

  return (
    <div className="mt-4">
      <h2 className="text-neutral-800 font-bold mt-4">Token Balances</h2>
      <div className="flex flex-col gap-2 mt-2">
        {tokenBalances && tokenBalances.length > 0 ? (
          tokenBalances.map((token) => (
            <div
              key={token.address}
              className="flex justify-between items-center"
            >
              <span className="text-neutral-800">{token.symbol}</span>
              <span className="text-neutral-800">{token.balance}</span>
            </div>
          ))
        ) : (
          <p className="text-neutral-800">No token balances found</p>
        )}
      </div>
    </div>
  );
}
