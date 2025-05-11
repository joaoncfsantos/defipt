import {
  Card as UICard,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface CardProps {
  title: string;
  description: string;
  onClick: () => void;
}

export function Card({ title, description, onClick }: CardProps) {
  return (
    <UICard
      className="w-full text-white bg-neutral-800 hover:bg-neutral-700 transition-colors duration-300 gap-2 cursor-pointer"
      onClick={onClick}
    >
      <CardHeader>
        <CardTitle className="text-2xl">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{description}</p>
      </CardContent>
    </UICard>
  );
}
