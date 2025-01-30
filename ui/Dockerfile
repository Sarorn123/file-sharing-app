FROM oven/bun:alpine

# Set the working directory
WORKDIR /app

# Copy the package.json (always present)
COPY package.json . 

# Copy bun.lockb only if it exists to avoid errors
COPY bun.lockb* . 

# Install dependencies
RUN bun install

# Copy the entire app after installing dependencies
COPY . .

# Build the React application
RUN bun run build

# Expose the port for the React app
EXPOSE 4173

# Serve the built app
CMD ["bun", "run", "preview", "--host", "0.0.0.0"]
